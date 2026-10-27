(async () => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const tap = id => { const l = document.getElementById(id).closest("label"); l.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true })); l.click(); };
  document.documentElement.style.scrollBehavior = "auto";
  window.AL_CONFIG.formsubmitTo = "t@example.com";
  window.fetch = (u, o) => { window.__body = o && o.body; return new Promise(r => setTimeout(() => r(new Response(JSON.stringify({ success: "true" }), { status: 200 })), 500)); };
  document.querySelector("#consent [data-c=reject]").click();
  const out = {};
  document.querySelector('.room-cta[data-room="ketagyas"]').click(); await wait(500);
  out.hash = location.hash;
  tap("wl-rel-self"); await wait(700);
  out.step2_preselected = document.getElementById("wl-room-2").checked;
  document.querySelector('[data-step="2"] [data-next]').click(); await wait(400);
  tap("wl-t-0"); await wait(700);
  document.getElementById("wl-name").value = "Kovácsné Szabó Éva";
  document.querySelector('[data-step="4"] [data-next]').click(); await wait(400);
  document.getElementById("wl-email").value = "a@b.hu"; document.getElementById("wl-phone").value = "+36301234567";
  document.querySelector('[data-step="5"] [data-next]').click(); await wait(400);
  document.getElementById("wl-pricing").click(); document.getElementById("wl-privacy").click();
  document.getElementById("form-varolista").requestSubmit(); await wait(150);
  const b = JSON.parse(window.__body || "{}");
  out.room = b["Szobatípus"]; out.origin = b["Honnan jelentkezett"];
  out.stored = sessionStorage.getItem("al_thanks");
  return out;
})()
