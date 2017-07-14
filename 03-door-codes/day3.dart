int o(String char) {
  return char.codeUnitAt(0) - 'a'.codeUnitAt(0) + 1;
}

int n(int rune) {
  return rune - 'a'.codeUnitAt(0) + 1;
}


String c(int num) {
  return new String.fromCharCode((num - 1) % 26 + 'a'.codeUnitAt(0));
}

var letters = new RegExp(r'[a-z]');

String code1(String expanded_passphrase) {
  String passphrase = letters.allMatches(expanded_passphrase).map((Match m) => m[0]).join();
  String c0 = passphrase[0];
  String c1 = passphrase[1];
  passphrase.substring(2).runes.forEach((int rune) {
    c0 = c(o(c0) + o(c1));
    c1 = c(o(c1) + n(rune));
  });
  return c0 + c1;
}

String code2(String expanded_passphrase) {
  String passphrase = letters.allMatches(expanded_passphrase).map((Match m) => m[0]).join();
  int alpha = 5;
  int beta = 11;
  String c0 = "r";
  String c1 = "i";
  passphrase.runes.forEach((int rune) {
    c0 = c(o(c0) + o(c1) * alpha);
    c1 = c(o(c1) + n(rune) * beta);
  });
  return c0 + c1;
}

void main() {
//   "abcdefghijklmnopqrstuvwxyz".runes.forEach((int rune) {
//     print('$rune : ${new String.fromCharCode(rune)} :: ${n(rune)} ${c(n(rune) + 28)}');
//   });
  
//   for (var match in letters.allMatches('The quick ! broWn')) {
//   	print(match.group(0)); // 15, then 20
// 	};
  
//   print(letters.allMatches('The quick ! broWn').map((Match m) => m[0]).join());
  
  String phr = "the traveller in the grey riding-coat, who called himself mr. melville, was "
                      "contemplating the malice of which the gods are capable.";
  
//  print(code1('the cat.'));
  print(code1(phr));
  
//  print(code2('the cat.'));
  print(code2(phr));
}
