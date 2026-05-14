function normalizeUrl(value) {
  value = String(value || '').trim();
  if (!value) return 'https://www.xbox.com/pt-BR/play';
  if (value.indexOf('://') === -1) value = 'https://' + value;
  return value;
}

function go(value) {
  window.location.href = normalizeUrl(value);
}

window.addEventListener('load', function () {
  var input = document.getElementById('url');
  var open = document.getElementById('open');
  var xcloud = document.getElementById('xcloud');
  var login = document.getElementById('login');

  if (open) open.addEventListener('click', function () {
    go(input ? input.value : 'https://www.xbox.com/pt-BR/play');
  });

  if (xcloud) xcloud.addEventListener('click', function () {
    go('https://www.xbox.com/pt-BR/play');
  });

  if (login) login.addEventListener('click', function () {
    var target = encodeURIComponent('https://www.xbox.com/pt-BR/play');
    go('https://www.xbox.com/pt-BR/auth/msa?action=logIn&returnUrl=' + target + '&ru=' + target);
  });
});
