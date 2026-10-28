/* ===== ÉLESÍTÉSI BEÁLLÍTÁSOK – minden oldal ezt a fájlt használja =====
   formsubmitTo       FormSubmit címzett: a fogadó e-mail-cím, vagy az aktiválás után kapott
                      véletlen azonosító (ez elrejti az e-mail-címet a forráskódból).
                      Az első beküldés után a FormSubmit aktiváló e-mailt küld – azt jóvá kell hagyni,
                      addig az űrlap nem fogad adatot.
   formsubmitCc       további címzettek vesszővel elválasztva (nem kötelező)
   autoresponse       a jelentkezőnek küldött automatikus visszaigazolás szövege ("" = nincs)
   submitEndpoint     saját backend / CRM webhook (JSON POST) – ha ki van töltve, a FormSubmit helyett ez fut
   metaPixelId        Meta Pixel azonosító (csak hozzájárulás után töltődik be)
   ga4MeasurementId   GA4 mérési azonosító (csak hozzájárulás után töltődik be)
   renders            látványtervek URL-jei; a képes blokkok csak kitöltve jelennek meg */
window.AL_CONFIG = {
  formsubmitTo: "mullerdanielev@gmail.com",          // pl. "info@aroktoiliget.hu" vagy "a1b2c3d4e5f6..."
  formsubmitCc: "",
  autoresponse: {
    varolista: "Köszönjük az Ároktői Liget Senior Rezidenciára leadott előzetes jelentkezését. A nyitás előtt elsőként értesítjük a beköltözés lehetőségéről, addig pedig a projekt előrehaladásáról is tájékoztatjuk. A jelentkezés nem jelent férőhelyfoglalást vagy garantált felvételt, és nem jár fizetési kötelezettséggel."
  },
  submitEndpoint: "",
  metaPixelId: "1181229674234476",
  ga4MeasurementId: "",      // pl. "G-XXXXXXXXXX"
  renders: { hero: "", intro: "", g1: "", g2: "", g3: "" }
};
