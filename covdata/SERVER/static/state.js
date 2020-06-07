$(document).ready(function () {
  var menu = document.querySelector(".hamburger-menu");
  var bar = document.querySelector(".nav-bar");
  menu.addEventListener("click", () => {
    bar.classList.toggle("change");
  });
  $("select").niceSelect();
  GetDataState();
  $("#daily").change(function () {
    GetDataState();
  });
  $("#state_name").change(function () {
    GetDataState();
  });
  $("svg").click(function () {
    // console.log($(this));
    var info = document.querySelector(".status");
    info.classList.remove("animate1");
    info.classList.remove("animate2");
    var reload = document.querySelector("svg");
    reload.classList.add("reload");
    $.get("/refresh/state", function (data, textStatus, jqXHR) {
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
  $(".download").click(function () {
    var e = document.getElementById("state_name");
    var p = document.getElementById("daily");
    var result = e.options[e.selectedIndex].text;
    var daily = p.options[p.selectedIndex].text;
    const a = document.createElement("a");
    a.style.display = "none";
    document.body.appendChild(a);
    a.href = "/get-csv/" + result + "-" + daily;
    // a.setAttribute("download", "Confirmed.csv");
    a.click();
    window.URL.revokeObjectURL(a.href);
    document.body.removeChild(a);
  });
});

function GetDataState() {
  var e = document.getElementById("state_name");
  var state_name = e.options[e.selectedIndex].text;

  var p = document.getElementById("daily");
  var daily = p.options[p.selectedIndex].text;

  $.post(
    "/State",
    {
      state_data: JSON.stringify(state_name),
      daily_data: JSON.stringify(daily),
    },
    function (data, status, xhr) {
      var df = JSON.parse(data);
      // Extract value from table header.
      var col = [];
      for (var i = 0; i < df.length; i++) {
        for (var key in df[i]) {
          if (col.indexOf(key) === -1) {
            col.push(key);
          }
        }
      }

      // Create a table.
      var table = document.createElement("table");

      // Create table header row using the extracted headers above.
      var tr = table.insertRow(-1); // table row.

      for (var i = 0; i < col.length; i++) {
        var th = document.createElement("th"); // table header.
        th.innerHTML = col[i];
        tr.appendChild(th);
      }

      // add json data to the table as rows.
      for (var i = 0; i < df.length; i++) {
        tr = table.insertRow(-1);

        for (var j = 0; j < col.length; j++) {
          var tabCell = tr.insertCell(-1);
          tabCell.innerHTML = df[i][col[j]];
        }
      }
      var divShowData = document.getElementById("data_show");
      console.log(JSON.parse(data));
      console.log(Object.keys(df[0]));
      divShowData.innerHTML = "";
      divShowData.appendChild(table);
      divShowData.style.width = "auto";
      divShowData.style.maxWidth = "80vw";
      divShowData.style.maxHeight = "500px";
      // divShowData.style.background = "grey";
      divShowData.style.overflow = "auto";
      divShowData.style.marginTop = "20px";
      // divShowData.style.marginLeft = "50%";
    }
  );
}
