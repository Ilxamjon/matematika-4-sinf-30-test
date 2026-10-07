# Lokal tarmoq serveri. Windows PowerShell 5.1. Internet va Python shart emas.
param(
  [switch]$LocalOnly,
  [switch]$NoBrowser
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$site = Join-Path $root 'sayt'
$results = Join-Path $root 'natijalar'
$port = 8787

if (-not (Test-Path (Join-Path $site 'index.html'))) {
  Write-Host "sayt\index.html topilmadi. ZIP faylni toliq oching."
  exit 1
}
New-Item -ItemType Directory -Force -Path $results | Out-Null

$code = @'
using System;
using System.Collections;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.NetworkInformation;
using System.Net.Sockets;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Web.Script.Serialization;

namespace LocalQuiz {
  public class Server {
    readonly string siteDir;
    readonly string sitePrefix;
    readonly string resultsDir;
    readonly int port;
    readonly List<Question> questions = new List<Question>();
    readonly Dictionary<string, Question> byId = new Dictionary<string, Question>();
    readonly ConcurrentDictionary<string, Session> sessions = new ConcurrentDictionary<string, Session>();
    readonly ConcurrentDictionary<string, Live> live = new ConcurrentDictionary<string, Live>();
    readonly object fileLock = new object();
    readonly object rngLock = new object();
    readonly Random rng = new Random();
    readonly JavaScriptSerializer json = new JavaScriptSerializer { MaxJsonLength = int.MaxValue };
    byte[] publicBank;
    HttpListener listener;
    volatile bool running;

    public Server(string siteDir, string resultsDir, int port) {
      this.siteDir = siteDir;
      this.sitePrefix = siteDir.TrimEnd('\\') + "\\";
      this.resultsDir = resultsDir;
      this.port = port;
      LoadBank();
    }

    public bool IsRunning { get { return running; } }

    public void Start(bool allInterfaces) {
      listener = new HttpListener();
      if (allInterfaces) listener.Prefixes.Add("http://+:" + port + "/");
      else listener.Prefixes.Add("http://127.0.0.1:" + port + "/");
      listener.Start();
      running = true;
      ThreadPool.QueueUserWorkItem(delegate { AcceptLoop(); });
    }

    public void Stop() {
      running = false;
      try { if (listener != null) listener.Stop(); } catch { }
      try { if (listener != null) listener.Close(); } catch { }
    }

    public List<string> Addresses() {
      var list = new List<string>();
      var seen = new HashSet<string>();
      try {
        foreach (NetworkInterface ni in NetworkInterface.GetAllNetworkInterfaces()) {
          if (ni.OperationalStatus != OperationalStatus.Up) continue;
          if (ni.NetworkInterfaceType == NetworkInterfaceType.Loopback) continue;
          foreach (UnicastIPAddressInformation ua in ni.GetIPProperties().UnicastAddresses) {
            if (ua.Address.AddressFamily != AddressFamily.InterNetwork) continue;
            string text = ua.Address.ToString();
            if (text.StartsWith("169.254.")) continue;
            if (seen.Add(text)) list.Add("http://" + text + ":" + port + "/");
          }
        }
      } catch { }
      return list;
    }

    void LoadBank() {
      string bankPath = Path.Combine(siteDir, "bank.json");
      string raw = File.ReadAllText(bankPath, Encoding.UTF8);
      int keys = Regex.Matches(raw, ",\"answer\":\"[A-E]\"").Count;
      string stripped = Regex.Replace(raw, ",\"answer\":\"[A-E]\"", "");
      if (stripped.IndexOf("\"answer\"", StringComparison.Ordinal) >= 0) throw new InvalidOperationException("Javob kaliti yashirilmadi.");
      var rows = json.Deserialize<List<Dictionary<string, object>>>(raw);
      if (rows == null || rows.Count != keys || rows.Count < 30) throw new InvalidOperationException("Savollar bazasi noto'g'ri.");
      foreach (Dictionary<string, object> row in rows) {
        var q = new Question();
        q.Id = Convert.ToString(row["id"]);
        q.Section = Convert.ToInt32(row["section"]);
        q.Answer = Convert.ToString(row["answer"]);
        q.Options = new HashSet<string>(StringComparer.Ordinal);
        foreach (object option in (IEnumerable)row["options"]) q.Options.Add(Convert.ToString(option));
        if (byId.ContainsKey(q.Id) || q.Answer.Length != 1 || !q.Options.Contains(q.Answer)) throw new InvalidOperationException("Savol yaroqsiz: " + q.Id);
        byId[q.Id] = q;
        questions.Add(q);
      }
      publicBank = Encoding.UTF8.GetBytes("window.LAN_MODE=true;window.QUESTION_BANK=" + stripped + ";");
    }

    void AcceptLoop() {
      while (running && listener != null && listener.IsListening) {
        HttpListenerContext ctx;
        try { ctx = listener.GetContext(); }
        catch { break; }
        ThreadPool.QueueUserWorkItem(delegate(object state) {
          var context = (HttpListenerContext)state;
          try { Handle(context); }
          catch { try { context.Response.Abort(); } catch { } }
        }, ctx);
      }
    }

    void Handle(HttpListenerContext ctx) {
      string method = ctx.Request.HttpMethod;
      string rel = Uri.UnescapeDataString(ctx.Request.Url.AbsolutePath).Trim('/');
      bool local = ctx.Request.IsLocal;
      if (rel == "api/holat" && method == "GET") { WriteJson(ctx, 200, Holat(local)); return; }
      if (rel == "api/boshlash" && method == "POST") { Begin(ctx); return; }
      if (rel == "api/jarayon" && method == "POST") { Progress(ctx); return; }
      if (rel == "api/natija" && method == "POST") { Finish(ctx); return; }
      if (rel == "api/natijalar" && method == "GET") { if (!local) { NotFound(ctx); return; } WriteJson(ctx, 200, Results()); return; }
      if (rel == "api/tozalash" && method == "POST") { if (!local) { NotFound(ctx); return; } Clear(ctx); return; }
      if (method != "GET" && method != "HEAD") { Text(ctx, 405, "text/plain; charset=utf-8", "Ruxsat etilmagan."); return; }
      if (rel == "oqituvchi" || rel == "oqituvchi.html") { if (!local) { NotFound(ctx); return; } SendFile(ctx, Path.Combine(siteDir, "oqituvchi.html"), method == "HEAD"); return; }
      if (rel == "" || rel == "index.html") { SendFile(ctx, Path.Combine(siteDir, "index.html"), method == "HEAD"); return; }
      if (rel == "bank.js") { Bytes(ctx, 200, "application/javascript; charset=utf-8", publicBank, "no-cache", method == "HEAD"); return; }
      if (rel == "favicon.ico") { Text(ctx, 204, "image/x-icon", ""); return; }
      if (rel.IndexOf("..", StringComparison.Ordinal) >= 0 || rel.EndsWith(".json", StringComparison.OrdinalIgnoreCase)) { NotFound(ctx); return; }
      string full = Path.GetFullPath(Path.Combine(siteDir, rel.Replace('/', '\\')));
      if (!full.StartsWith(sitePrefix, StringComparison.OrdinalIgnoreCase) || !File.Exists(full)) { NotFound(ctx); return; }
      SendFile(ctx, full, method == "HEAD");
    }

    Dictionary<string, object> Holat(bool local) {
      var body = new Dictionary<string, object>();
      body["lan"] = true;
      body["savollar"] = questions.Count;
      body["manzillar"] = Addresses();
      body["tozalash"] = local;
      return body;
    }

    void Begin(HttpListenerContext ctx) {
      Cleanup();
      Dictionary<string, object> data = ReadJson(ctx);
      if (data == null) { WriteJson(ctx, 400, Error("So\u2018rov o\u2018qilmadi.")); return; }
      string ism = Clean(Value(data, "ism"), 80);
      string sinf = Clean(Value(data, "sinf"), 20);
      if (ism.Length < 2) { WriteJson(ctx, 400, Error("Ism familiyani kiriting.")); return; }
      int section;
      try { section = Convert.ToInt32(data["section"]); }
      catch { WriteJson(ctx, 400, Error("Mavzu noto\u2018g\u2018ri.")); return; }
      if (section < -1 || section == 0 || section > 129) { WriteJson(ctx, 400, Error("Mavzu noto\u2018g\u2018ri.")); return; }
      var pool = new List<Question>();
      foreach (Question q in questions) {
        if (section < 0 || q.Section == section) pool.Add(q);
      }
      int take = pool.Count < 30 ? pool.Count : 30;
      if (take < 1) { WriteJson(ctx, 400, Error("Bu mavzuda savol yo\u2018q.")); return; }
      lock (rngLock) {
        for (int i = pool.Count - 1; i > 0; i--) {
          int j = rng.Next(i + 1);
          Question tmp = pool[i];
          pool[i] = pool[j];
          pool[j] = tmp;
        }
      }
      var session = new Session();
      session.Id = Guid.NewGuid().ToString("N");
      session.Ism = ism;
      session.Sinf = sinf;
      session.Mavzu = section < 0 ? "Barcha mavzular" : Clean(Value(data, "mavzu"), 160);
      if (session.Mavzu.Length == 0) session.Mavzu = section + "-§";
      session.Ids = new List<string>();
      for (int i = 0; i < take; i++) session.Ids.Add(pool[i].Id);
      session.StartedUtc = DateTime.UtcNow;
      sessions[session.Id] = session;
      var ids = new ArrayList();
      foreach (string id in session.Ids) ids.Add(id);
      var body = new Dictionary<string, object>();
      body["session"] = session.Id;
      body["ids"] = ids;
      WriteJson(ctx, 200, body);
    }

    void Progress(HttpListenerContext ctx) {
      Dictionary<string, object> data = ReadJson(ctx);
      if (data == null) { WriteJson(ctx, 400, Error("So\u2018rov o\u2018qilmadi.")); return; }
      Session session;
      if (!sessions.TryGetValue(Value(data, "session"), out session) || session.Done) { WriteJson(ctx, 404, Error("Test topilmadi.")); return; }
      int answered = 0, current = 1;
      try { answered = Convert.ToInt32(data["javob"]); } catch { answered = 0; }
      try { current = Convert.ToInt32(data["savol"]); } catch { current = 1; }
      int limit = session.Ids.Count;
      if (answered < 0) answered = 0;
      if (answered > limit) answered = limit;
      if (current < 1) current = 1;
      if (current > limit) current = limit;
      var row = new Live();
      row.Ism = session.Ism;
      row.Sinf = session.Sinf;
      row.Mavzu = session.Mavzu;
      row.Javob = answered;
      row.Savol = current;
      row.Jami = limit;
      row.SeenUtc = DateTime.UtcNow;
      live[session.Id] = row;
      WriteJson(ctx, 200, new Dictionary<string, object> { { "ok", true } });
    }

    void Finish(HttpListenerContext ctx) {
      Dictionary<string, object> data = ReadJson(ctx);
      if (data == null) { WriteJson(ctx, 400, Error("So\u2018rov o\u2018qilmadi.")); return; }
      Session session;
      if (!sessions.TryGetValue(Value(data, "session"), out session)) { WriteJson(ctx, 404, Error("Test topilmadi. Qaytadan boshlang.")); return; }
      object rawAnswers;
      if (!data.TryGetValue("javoblar", out rawAnswers) || !(rawAnswers is ArrayList)) { WriteJson(ctx, 400, Error("Javoblar noto\u2018g\u2018ri.")); return; }
      var answers = (ArrayList)rawAnswers;
      if (answers.Count != session.Ids.Count || answers.Count < 1) { WriteJson(ctx, 400, Error("Javoblar soni noto\u2018g\u2018ri.")); return; }
      int total = session.Ids.Count;
      var choices = new string[total];
      for (int i = 0; i < total; i++) {
        if (answers[i] == null) { choices[i] = null; continue; }
        choices[i] = Convert.ToString(answers[i]);
        if (choices[i].Length == 0) choices[i] = null;
        else if (!byId[session.Ids[i]].Options.Contains(choices[i])) { WriteJson(ctx, 400, Error("Javob varianti noto\u2018g\u2018ri.")); return; }
      }
      lock (fileLock) {
      if (session.Done) {
        if (Same(session.Choices, choices)) { WriteJson(ctx, 200, session.Response); return; }
        WriteJson(ctx, 409, Error("Bu test allaqachon yakunlangan."));
        return;
      }
      int correct = 0, empty = 0, wrong = 0;
      var keys = new Dictionary<string, object>();
      var detail = new ArrayList();
      for (int i = 0; i < total; i++) {
        Question q = byId[session.Ids[i]];
        bool hit = choices[i] != null && choices[i] == q.Answer;
        if (choices[i] == null) empty++;
        else if (hit) correct++;
        else wrong++;
        keys[q.Id] = q.Answer;
        var item = new Dictionary<string, object>();
        item["id"] = q.Id;
        item["tanlov"] = choices[i];
        item["kalit"] = q.Answer;
        item["togri"] = hit;
        detail.Add(item);
      }
      int seconds = (int)Math.Max(0, (DateTime.UtcNow - session.StartedUtc).TotalSeconds);
      var record = new Dictionary<string, object>();
      record["vaqt"] = DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss");
      record["ism"] = session.Ism;
      record["sinf"] = session.Sinf;
      record["mavzu"] = session.Mavzu;
      record["togri"] = correct;
      record["notogri"] = wrong;
      record["javobsiz"] = empty;
      record["foiz"] = (int)Math.Round(correct * 100.0 / total);
      record["jami"] = total;
      record["soniya"] = seconds;
      record["javoblar"] = detail;
      string name = DateTime.Now.ToString("yyyyMMdd-HHmmss-fff") + "-" + session.Id.Substring(0, 8) + ".json";
      File.WriteAllText(Path.Combine(resultsDir, name), json.Serialize(record), new UTF8Encoding(false));
      var response = new Dictionary<string, object>();
      response["togri"] = correct;
      response["notogri"] = wrong;
      response["javobsiz"] = empty;
      response["foiz"] = record["foiz"];
      response["kalit"] = keys;
      session.Choices = choices;
      session.Response = response;
      session.Done = true;
      Live ignore;
      live.TryRemove(session.Id, out ignore);
      Console.WriteLine("Natija: " + session.Ism + (session.Sinf.Length > 0 ? " (" + session.Sinf + ")" : "") + " - " + correct + "/" + total);
      WriteJson(ctx, 200, response);
      }
    }

    Dictionary<string, object> Results() {
      Cleanup();
      var rows = new ArrayList();
      lock (fileLock) {
        if (Directory.Exists(resultsDir)) {
          string[] files = Directory.GetFiles(resultsDir, "*.json");
          Array.Sort(files);
          Array.Reverse(files);
          foreach (string file in files) {
            try {
              var row = json.Deserialize<Dictionary<string, object>>(File.ReadAllText(file, Encoding.UTF8));
              if (row != null && row.ContainsKey("ism")) {
                row.Remove("javoblar");
                rows.Add(row);
              }
            } catch { }
          }
        }
      }
      var active = new ArrayList();
      DateTime fresh = DateTime.UtcNow.AddSeconds(-40);
      foreach (KeyValuePair<string, Live> pair in live) {
        if (pair.Value.SeenUtc < fresh) continue;
        var row = new Dictionary<string, object>();
        row["ism"] = pair.Value.Ism;
        row["sinf"] = pair.Value.Sinf;
        row["mavzu"] = pair.Value.Mavzu;
        row["javob"] = pair.Value.Javob;
        row["savol"] = pair.Value.Savol;
        row["jami"] = pair.Value.Jami;
        active.Add(row);
      }
      var body = new Dictionary<string, object>();
      body["natijalar"] = rows;
      body["jarayonda"] = active;
      return body;
    }

    void Clear(HttpListenerContext ctx) {
      lock (fileLock) {
        if (Directory.Exists(resultsDir)) {
          foreach (string file in Directory.GetFiles(resultsDir, "*.json")) File.Delete(file);
        }
      }
      WriteJson(ctx, 200, new Dictionary<string, object> { { "ok", true } });
    }

    void Cleanup() {
      DateTime old = DateTime.UtcNow.AddHours(-8);
      foreach (KeyValuePair<string, Session> pair in sessions) {
        if (pair.Value.StartedUtc >= old) continue;
        Session removed;
        sessions.TryRemove(pair.Key, out removed);
      }
      DateTime stale = DateTime.UtcNow.AddMinutes(-2);
      foreach (KeyValuePair<string, Live> pair in live) {
        if (pair.Value.SeenUtc >= stale) continue;
        Live removed;
        live.TryRemove(pair.Key, out removed);
      }
    }

    static bool Same(string[] saved, string[] next) {
      if (saved == null || next == null || saved.Length != next.Length) return false;
      for (int i = 0; i < saved.Length; i++) if (saved[i] != next[i]) return false;
      return true;
    }

    static string Value(Dictionary<string, object> data, string key) {
      object value;
      if (!data.TryGetValue(key, out value) || value == null) return "";
      return Convert.ToString(value);
    }

    static string Clean(string value, int max) {
      if (value == null) return "";
      value = value.Trim().Replace("\r", " ").Replace("\n", " ").Replace("\t", " ");
      if (value.Length > max) value = value.Substring(0, max);
      return value;
    }

    Dictionary<string, object> ReadJson(HttpListenerContext ctx) {
      try {
        var buffer = new MemoryStream();
        byte[] chunk = new byte[8192];
        int total = 0;
        int read;
        while ((read = ctx.Request.InputStream.Read(chunk, 0, chunk.Length)) > 0) {
          total += read;
          if (total > 200000) return null;
          buffer.Write(chunk, 0, read);
        }
        if (total == 0) return null;
        return json.Deserialize<Dictionary<string, object>>(Encoding.UTF8.GetString(buffer.ToArray()));
      } catch { return null; }
    }

    static Dictionary<string, object> Error(string message) {
      return new Dictionary<string, object> { { "xato", message } };
    }

    void WriteJson(HttpListenerContext ctx, int code, object body) {
      Bytes(ctx, code, "application/json; charset=utf-8", Encoding.UTF8.GetBytes(json.Serialize(body)), "no-store", false);
    }

    void SendFile(HttpListenerContext ctx, string path, bool head) {
      string type = Mime(path);
      string cache = type.StartsWith("image/") ? "public, max-age=86400" : "no-cache";
      byte[] data = File.ReadAllBytes(path);
      Bytes(ctx, 200, type, data, cache, head);
    }

    static string Mime(string path) {
      switch (Path.GetExtension(path).ToLowerInvariant()) {
        case ".html": return "text/html; charset=utf-8";
        case ".css": return "text/css; charset=utf-8";
        case ".js": return "application/javascript; charset=utf-8";
        case ".webp": return "image/webp";
        case ".png": return "image/png";
        case ".jpg":
        case ".jpeg": return "image/jpeg";
        case ".svg": return "image/svg+xml";
        default: return "application/octet-stream";
      }
    }

    void NotFound(HttpListenerContext ctx) { Text(ctx, 404, "text/plain; charset=utf-8", "Topilmadi."); }

    void Text(HttpListenerContext ctx, int code, string type, string body) {
      Bytes(ctx, code, type, Encoding.UTF8.GetBytes(body), "no-store", false);
    }

    void Bytes(HttpListenerContext ctx, int code, string type, byte[] data, string cache, bool head) {
      HttpListenerResponse res = ctx.Response;
      res.StatusCode = code;
      res.ContentType = type;
      res.Headers["Cache-Control"] = cache;
      res.ContentLength64 = data.Length;
      if (!head && data.Length > 0) res.OutputStream.Write(data, 0, data.Length);
      res.Close();
    }

    class Question {
      public string Id;
      public int Section;
      public string Answer;
      public HashSet<string> Options;
    }

    class Session {
      public string Id;
      public string Ism;
      public string Sinf;
      public string Mavzu;
      public List<string> Ids;
      public DateTime StartedUtc;
      public bool Done;
      public string[] Choices;
      public Dictionary<string, object> Response;
    }

    class Live {
      public string Ism;
      public string Sinf;
      public string Mavzu;
      public int Javob;
      public int Savol;
      public int Jami;
      public DateTime SeenUtc;
    }
  }
}
'@

$compiled = $false
foreach ($dll in @(
  'System.Web.Extensions',
  (Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\System.Web.Extensions.dll'),
  (Join-Path $env:WINDIR 'Microsoft.NET\Framework\v4.0.30319\System.Web.Extensions.dll')
)) {
  if ($compiled) { break }
  if ($dll -ne 'System.Web.Extensions' -and -not (Test-Path $dll)) { continue }
  try {
    Add-Type -TypeDefinition $code -ReferencedAssemblies $dll -ErrorAction Stop
    $compiled = $true
  } catch {
    if ($dll -eq 'System.Web.Extensions') { continue }
    throw
  }
}
if (-not $compiled) { throw 'Server kodini yigib bolmadi.' }

$server = New-Object LocalQuiz.Server($site, $results, $port)
$lan = -not $LocalOnly
if ($lan) {
  $rule = 'Informatika-30-test'
  $null = netsh advfirewall firewall delete rule name="$rule" 2>$null
  $null = netsh advfirewall firewall add rule name="$rule" dir=in action=allow protocol=TCP localport=$port profile=any
  if ($LASTEXITCODE -ne 0) {
    Write-Host "Ogohlantirish: Windows xavfsizlik devori qoidasi qo'shilmadi."
    Write-Host "Boshqa kompyuterlar ulanolmasligi mumkin."
  }
}
try {
  $server.Start($lan)
} catch {
  Write-Host "Server ochilmadi. 3_LOKAL_TARMOQ.cmd ni administrator sifatida qayta ishga tushiring."
  Write-Host $_.Exception.Message
  exit 1
}

Write-Host ""
Write-Host "LOKAL TARMOQ ISHGA TUSHDI"
Write-Host "Oquvchilar brauzerda shu manzilni ochadi:"
$addresses = @($server.Addresses())
if ($addresses.Count -eq 0) {
  Write-Host "  (Wi-Fi yoki lokal tarmoq manzili topilmadi. Kompyuterni tarmoqqa ulang.)"
} else {
  foreach ($address in $addresses) { Write-Host "  $address" }
}
Write-Host "Oqituvchi natijalari (shu kompyuterdan):"
Write-Host "  http://127.0.0.1:$port/oqituvchi"
Write-Host "Toxtatish: Ctrl+C"
Write-Host ""

if (-not $NoBrowser) {
  Start-Process "http://127.0.0.1:$port/"
}
try {
  while ($server.IsRunning) { Start-Sleep -Milliseconds 500 }
} finally {
  $server.Stop()
  if ($lan) { $null = netsh advfirewall firewall delete rule name='Informatika-30-test' 2>$null }
}
