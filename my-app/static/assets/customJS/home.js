const loaderOut = document.querySelector("#loader-out");
function fadeOut(element) {
  let opacity = 1;
  const timer = setInterval(function () {
    if (opacity <= 0.1) {
      clearInterval(timer);
      element.style.display = "none";
    }
    element.style.opacity = opacity;
    opacity -= opacity * 0.1;
  }, 50);
}
fadeOut(loaderOut);

function ParaImpresion(id_impresion) {
  if (confirm("¿Estas seguro que deseas parar la impresion?")) {
    let url = `/parar-impresion/${id_impresion}`;
    if (url) {
      window.location.href = url;
    }
  }
}


function Reemprimir_Impresion(id_impresion) {
  if (confirm("¿Estas seguro que deseas Reemprimir?")) {
    let url = `/reemprimir-impresion/${id_impresion}`;
    if (url) {
      window.location.href = url;
    }
  }
}