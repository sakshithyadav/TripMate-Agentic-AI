/* Load AFTER script.js. Wraps its functions to add animations; script.js stays unchanged. */
(() => {
  const $ = (id) => document.getElementById(id);
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const STEPS = {
    draft: ["Supervisor is picking the right agents…", "Searching flights…", "Comparing hotels…", "Checking the weather…", "Balancing your budget…", "Drafting your itinerary…"],
    approve: ["Locking in your plan…", "Writing the final itinerary…"],
    revise: ["Reading your feedback…", "Rebuilding the plan…"]
  };
  let timer = null;
  let lastAction = null;

  function restart(el, cls) {
    el.classList.remove(cls);
    void el.offsetWidth;
    el.classList.add(cls);
  }

  function startOverlay(mode) {
    const box = $("flightOverlay");
    const text = $("overlayText");
    let i = 0;
    box.dataset.mode = mode;
    const say = () => {
      text.textContent = STEPS[mode][i++ % STEPS[mode].length];
      restart(text, "swap");
    };
    say();
    clearInterval(timer);
    timer = setInterval(say, 2400);
    box.classList.add("on");
  }

  function stopOverlay() {
    clearInterval(timer);
    $("flightOverlay").classList.remove("on");
  }

  // Show the overlay only when the request really started (the button gets disabled).
  function track(name, busyBtnId, modeOf) {
    const orig = window[name];
    window[name] = function (...args) {
      const mode = modeOf(args);
      if (mode === "draft") lastAction = null;
      else lastAction = mode;
      const p = orig.apply(this, args);
      if ($(busyBtnId).disabled) {
        startOverlay(mode);
        Promise.resolve(p).finally(stopOverlay);
      }
      return p;
    };
  }

  function confetti(count, colors) {
    if (calm) return;
    const c = document.createElement("canvas");
    c.className = "confetti";
    c.width = innerWidth;
    c.height = innerHeight;
    document.body.appendChild(c);
    const g = c.getContext("2d");
    const bits = Array.from({ length: count }, () => ({
      x: c.width / 2, y: c.height * 0.45,
      vx: (Math.random() - 0.5) * 18, vy: -Math.random() * 14 - 4,
      r: Math.random() * 6 + 5, a: Math.random() * 6, va: (Math.random() - 0.5) * 0.4,
      col: colors[(Math.random() * colors.length) | 0]
    }));
    let frame = 0;
    (function tick() {
      g.clearRect(0, 0, c.width, c.height);
      bits.forEach((p) => {
        p.vy += 0.28; p.vx *= 0.99; p.x += p.vx; p.y += p.vy; p.a += p.va;
        g.save(); g.translate(p.x, p.y); g.rotate(p.a);
        g.fillStyle = p.col; g.fillRect(-p.r / 2, -p.r / 4, p.r, p.r / 2);
        g.restore();
      });
      if (++frame < 150) requestAnimationFrame(tick); else c.remove();
    })();
  }

  function stamp(text, cls) {
    const s = document.createElement("div");
    s.className = "stamp " + cls;
    s.textContent = text;
    document.body.appendChild(s);
    setTimeout(() => s.remove(), 2300);
  }

  function celebrate(kind) {
    if (kind === "approve") {
      stamp("Approved", "ok");
      confetti(150, ["#1f4fff", "#ffb627", "#0e1f3a", "#22c55e", "#ffffff"]);
    } else if (kind === "revise") {
      stamp("Revised", "rev");
      confetti(50, ["#1f4fff", "#ffb627"]);
    }
  }

  track("sendMessage", "sendBtn", () => "draft");
  track("submitApproval", "approveBtn", (args) => (args[0] ? "approve" : "revise"));

  const showWorkflow = window.showWorkflow;
  window.showWorkflow = function (...args) {
    showWorkflow.apply(this, args);
    document.querySelectorAll("#agentChips .agent-chip").forEach((chip, i) => chip.style.setProperty("--i", i));
  };

  const showResult = window.showResult;
  window.showResult = function (answer, threadId, isDraft) {
    showResult.apply(this, arguments);
    restart($("resultSection"), "unfold");
    if (!isDraft) celebrate(lastAction);
  };

  const showApproval = window.showApproval;
  window.showApproval = function (...args) {
    showApproval.apply(this, args);
    restart($("approvalSection"), "attn");
  };
})();