function openXcloud() {
  var locale = '/pt-BR';
  var returnUrl = encodeURIComponent('https://www.xbox.com' + locale + '/play');
  var url = 'https://www.xbox.com' + locale + '/auth/msa?action=logIn&returnUrl=' + returnUrl + '&ru=' + returnUrl;
  location.href = url;
}

window.addEventListener('load', function () {
  var button = document.getElementById('open');
  if (button) button.addEventListener('click', openXcloud);
});
