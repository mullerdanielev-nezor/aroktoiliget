/* ===== ÉLESÍTÉSI BEÁLLÍTÁSOK – minden oldal ezt a fájlt használja =====
   formsubmitTo       FormSubmit címzett: a fogadó e-mail-cím, vagy az aktiválás után kapott
                      véletlen azonosító (ez elrejti az e-mail-címet a forráskódból).
                      Az első beküldés után a FormSubmit aktiváló e-mailt küld – azt jóvá kell hagyni,
                      addig az űrlap nem fogad adatot.
   formsubmitCc       további címzettek vesszővel elválasztva (nem kötelező)
   autoresponse       a jelentkezőnek küldött automatikus visszaigazolás szövege ("" = nincs)
   formspreeEndpoint  Formspree űrlapcím (pl. "https://formspree.io/f/xyzabcd") – ha ki van töltve, a FormSubmit
                      helyett ez fut. A Formspree-ben a reCAPTCHA-t ki kell kapcsolni, különben nem fogad adatot.
   submitEndpoint     saját backend / CRM webhook (JSON POST) – ha ki van töltve, minden más helyett ez fut
   metaPixelId        Meta Pixel azonosító (csak hozzájárulás után töltődik be)
   ga4MeasurementId   GA4 mérési azonosító (csak hozzájárulás után töltődik be)
   renders            látványtervek URL-jei; a képes blokkok csak kitöltve jelennek meg */
window.AL_CONFIG = {
  /* Üres = nincs visszaigazoló e-mail a jelentkezőnek. Visszakapcsolás: "mullerdanielev@gmail.com" (FormSubmit). */
  formsubmitTo: "",          // pl. "info@aroktoiliget.hu" vagy "a1b2c3d4e5f6..."
  formsubmitCc: "",
  autoresponse: {
    /* {nev} helyére a jelentkező neve kerül */
    varolista: "Kedves {nev}!\n\nKöszönjük, hogy előzetesen jelentkezett az Ároktői Liget Senior Rezidenciára. Adatait rögzítettük.\n\nA nyitás előtt elsőként értesítjük a beköltözés lehetőségéről, addig pedig a projekt előrehaladásáról is tájékoztatjuk.\n\nA jelentkezés nem jelent helyfoglalást vagy garantált felvételt, és nem jár fizetési kötelezettséggel. Ha kérdése van, vagy szeretné, hogy töröljük az adatait, válaszoljon erre a levélre.\n\nÜdvözlettel:\nÁroktői Liget Senior Rezidencia\nZeusz Group Kft."
  },
  formspreeEndpoint: "https://formspree.io/f/xvkkrobg",
  submitEndpoint: "",
  metaPixelId: "1181229674234476",
  ga4MeasurementId: "",      // pl. "G-XXXXXXXXXX"
  renders: { hero: "", intro: "", g1: "", g2: "", g3: "" }
};
