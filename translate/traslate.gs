function doPost(e) {
  var p = JSON.parse(e.postData.getDataAsString());
  var translatedText = LanguageApp.translate(p.text, p.source, p.target);
  writeToSheet(translatedText);
}

var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
var sheet = spreadsheet.getSheets()[0]
var lastRow = sheet.getLastRow();
var lastColumn = sheet.getLastColumn();

function writeToSheet(sentence){
  sheet.getRange(lastRow+1, lastColumn).setValue(sentence);
  lastRow = sheet.getLastRow();
}

function doGet() {
  var translatedText = sheet.getRange(lastRow, lastColumn).getValue();
  var json = {
    translatedText: translatedText,
    textLang: "en",
    translatedLang: "ja"
  }
  return ContentService.createTextOutput(JSON.stringify(json)).setMimeType(ContentService.MimeType.JSON);
}