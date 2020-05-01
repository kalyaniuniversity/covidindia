// var e = document.getElementById("sheet-content");

// // var result = e.options[e.selectedIndex].text;

// console.log(e);
$(document).ready(function () {
  $("li:eq(0)").addClass("active");
});

function GetSelectedText() {
  var e = document.getElementById("sheet-content");
  // console.log(e);
  var result = e.options[e.selectedIndex].text;
  $.post(
    "/",
    {
      result_data: JSON.stringify(result),
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
      console.log(Object.values(df[0]));
      divShowData.innerHTML = "";
      divShowData.appendChild(table);
      divShowData.style.width = "auto";
      // divShowData.style.background = "grey";
      divShowData.style.overflow = "auto";
      divShowData.style.marginTop = "20px";
    }
  );

  //   console.log(result);
  // document.getElementById("result").innerHTML = result;
}
