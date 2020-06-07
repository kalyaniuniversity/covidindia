$(document).ready(function () {
  // $("li:eq(0)").addClass("active");
  var menu = document.querySelector(".hamburger-menu");
  var bar = document.querySelector(".nav-bar");
  menu.addEventListener("click", () => {
    bar.classList.toggle("change");
  });
  $("svg").click(function () {
    // console.log($(this));
    var info = document.querySelector(".status");
    info.classList.remove("animate1");
    info.classList.remove("animate2");
    var reload = document.querySelector("svg");
    reload.classList.add("reload");
    $.get("/refresh/home", function (data, textStatus, jqXHR) {
      if (data == "Updated") {
        $(".status").text("Already Updated");
        info.classList.add("animate1");
      } else {
        location.reload();
      }

      // $(".status").text(null);
      reload.classList.remove("reload");
      // info.classList.remove("animate");
    });
  });
});
