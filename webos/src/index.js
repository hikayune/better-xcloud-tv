function openXcloud() {
  location.href = 'https://www.xbox.com/play';
}

window.addEventListener('load', function () {
  var button = document.getElementById('open');
  if (button) button.addEventListener('click', openXcloud);
});
