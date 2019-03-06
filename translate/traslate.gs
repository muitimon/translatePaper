function doGet(e) {
  var p = e.parameter;
  var translatedText = LanguageApp.translate(p.text, p.source, p.target);
  json = {
    text: p.text,
    translatedText: translatedText,
    textLang: p.source,
    translatedLang: p.target
  }
  return ContentService.createTextOutput(JSON.stringify(json)).setMimeType(ContentService.MimeType.JSON);
}