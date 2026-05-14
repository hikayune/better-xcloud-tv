function openXcloud() {
  var base = 'https://www.xbox.com';
  var path = '/play/login/' + 'deviceCode';
  location.href = base + path;
}

window.addEventListener('load', function () {
  var button = document.getElementById('open');
  if (button) button.addEventListener('click', openXcloud);
});
