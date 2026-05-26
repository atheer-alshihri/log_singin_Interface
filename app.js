/* ── In-memory user store ─────────────────────────────────── */
const users = {};

/* ── Utilities ────────────────────────────────────────────── */
const $ = (id) => document.getElementById(id);
const isEmail = (v) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);

async function hashPassword(password) {
  const buf = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(password)
  );
  return Array.from(new Uint8Array(buf))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

function passwordStrength(pw) {
  let s = 0;
  if (pw.length >= 6) s++;
  if (/[A-Z]/.test(pw) || /[0-9]/.test(pw)) s++;
  if (pw.length >= 10 && /[^a-zA-Z0-9]/.test(pw)) s++;
  return s; // 0-3
}

/* ── Alert ────────────────────────────────────────────────── */
function showAlert(msg, type = "success") {
  const el = $("alert");
  el.className = `alert ${type}`;
  el.innerHTML = `<i class="ti ti-${type === "success" ? "circle-check" : "alert-circle"}"></i> ${msg}`;
  el.scrollIntoView({ block: "nearest", behavior: "smooth" });
}

function clearAlert() {
  $("alert").className = "alert hidden";
}

/* ── Tab switching ────────────────────────────────────────── */
const DOTS = { login: "dot-login", register: "dot-register", forgot: "dot-forgot" };

function showTab(name) {
  document.querySelectorAll(".tab").forEach((t) => {
    const active = t.dataset.tab === name;
    t.classList.toggle("active", active);
    t.setAttribute("aria-selected", active);
  });

  document.querySelectorAll(".panel").forEach((p) => {
    p.classList.toggle("active", p.id === `panel-${name}`);
  });

  Object.entries(DOTS).forEach(([key, id]) => {
    $(`${id}`).classList.toggle("active", key === name);
  });

  clearAlert();
}

/* ── Password visibility toggle ──────────────────────────── */
document.querySelectorAll(".toggle-pass").forEach((btn) => {
  btn.addEventListener("click", () => {
    const inp = $(btn.dataset.target);
    const isHidden = inp.type === "password";
    inp.type = isHidden ? "text" : "password";
    btn.querySelector("i").className = `ti ti-eye${isHidden ? "-off" : ""}`;
  });
});

/* ── Password strength meter ──────────────────────────────── */
$("r-pass").addEventListener("input", () => {
  const pw = $("r-pass").value;
  const s = passwordStrength(pw);
  const bars = [$("bar1"), $("bar2"), $("bar3")];
  const cls = ["weak", "medium", "strong"];
  const labels = ["", "Weak", "Fair", "Strong"];

  bars.forEach((b, i) => {
    b.className = "bar" + (i < s ? ` ${cls[s - 1]}` : "");
  });

  $("strength-text").textContent = pw.length ? labels[s] : "";
  $("strength-text").style.color =
    s === 1 ? "#ef4444" : s === 2 ? "#f59e0b" : s === 3 ? "#22c55e" : "";
});

/* ── Login ────────────────────────────────────────────────── */
$("btn-login").addEventListener("click", async () => {
  const email = $("l-email").value.trim();
  const pw    = $("l-pass").value;

  if (!email || !pw)         return showAlert("Please fill in all fields.", "error");
  if (!isEmail(email))       return showAlert("Enter a valid email address.", "error");
  if (!users[email])         return showAlert("No account found with that email.", "error");

  const hash = await hashPassword(pw);
  if (users[email].hash !== hash)
    return showAlert("Incorrect password. Please try again.", "error");

  showAlert(`Welcome back, ${users[email].name}! 🎉`);
});

/* ── Register ─────────────────────────────────────────────── */
$("btn-register").addEventListener("click", async () => {
  const fname = $("r-fname").value.trim();
  const lname = $("r-lname").value.trim();
  const email = $("r-email").value.trim();
  const pw    = $("r-pass").value;
  const pw2   = $("r-pass2").value;
  const terms = $("terms").checked;

  if (!fname || !email || !pw || !pw2)
    return showAlert("Please fill in all required fields.", "error");
  if (!isEmail(email))
    return showAlert("Enter a valid email address.", "error");
  if (pw !== pw2)
    return showAlert("Passwords do not match.", "error");
  if (pw.length < 6)
    return showAlert("Password must be at least 6 characters.", "error");
  if (!terms)
    return showAlert("You must agree to the Terms & Conditions.", "error");
  if (users[email])
    return showAlert("An account with this email already exists.", "error");

  const hash = await hashPassword(pw);
  users[email] = { name: `${fname} ${lname}`.trim(), hash };
  showAlert(`Account created! Welcome, ${fname} 🎉`);
});

/* ── Forgot password ──────────────────────────────────────── */
$("btn-forgot").addEventListener("click", () => {
  const email = $("f-email").value.trim();
  if (!email || !isEmail(email))
    return showAlert("Enter a valid email address.", "error");
  showAlert(`Reset link sent to ${email} ✉️`);
});

/* ── Social buttons ───────────────────────────────────────── */
document.querySelectorAll(".btn-social").forEach((btn) => {
  btn.addEventListener("click", () => {
    const provider = btn.querySelector("i").classList.contains("ti-brand-google")
      ? "Google" : "GitHub";
    showAlert(`${provider} sign-in coming soon!`, "error");
  });
});

/* ── Wire up tabs + navigation links ─────────────────────── */
document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => showTab(tab.dataset.tab));
});

document.querySelectorAll("[data-goto]").forEach((btn) => {
  btn.addEventListener("click", () => showTab(btn.dataset.goto));
});
