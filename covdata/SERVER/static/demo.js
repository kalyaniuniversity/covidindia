$(document).ready(function () {
  $("li:eq(2)").addClass("active");
  $("#state-name").change(function () {
    var el = $(this);
    // console.log(el.val());
    if (el.val() != "All") {
      $.post(
        "/filter",
        {
          place_data: el.val(),
        },
        function (data, status, xhr) {
          console.log(data);
          var children = document.getElementById("dis-span").children;
          console.log(children);
          if (children[children.length - 1] == undefined) {
            $("#dis-span").append(
              "<select id='district-select'><option>--Select District--</option><option>All</option></select>"
            );
          }
          $("#district-select option").each(function () {
            if (
              $(this).val() != "--Select District--" &&
              $(this).val() != "All"
            ) {
              $(this).remove();
            }
          });
          for (var i = 0; i < data.length; i++) {
            if (data[i] != "Unknown") {
              $("#district-select").append("<option>" + data[i] + "</option>");
            }
          }
          console.log(document.getElementById("district-select"));
          $("#district-select").change(function () {
            var el = $(this);
            console.log(el.val());
            if (el.val() != "All") {
              $.post(
                "/filter",
                {
                  place_data: el.val(),
                },
                function (data, status, xhr) {
                  console.log(data);
                  var children = document.getElementById("dis-span").children;
                  console.log(children);
                  if (
                    children[children.length - 1].getAttribute("id") !=
                    "city-select"
                  ) {
                    $("#dis-span").append(
                      "<select id='city-select'><option>--Select city--</option><option>All</option></select>"
                    );
                  }
                  $("#city-select option").each(function () {
                    if (
                      $(this).val() != "--Select city--" &&
                      $(this).val() != "All"
                    ) {
                      $(this).remove();
                    }
                  });
                  for (var i = 0; i < data.length; i++) {
                    if (data[i] != "Unknown") {
                      $("#city-select").append(
                        "<option>" + data[i] + "</option>"
                      );
                    }
                  }
                }
              );
            }
            if (el.val() === "All") {
              var children = document.getElementById("dis-span").children;
              if (
                children[children.length - 1].getAttribute("id") !=
                "district-select"
              ) {
                $("#dis-span select:last-child").remove();
              }
            }
          });
        }
      );
    }
    if (el.val() === "All") {
      $("#dis-span select:last-child").remove();
      $("#dis-span select:last-child").remove();
    }
  });
  $(document).ready(function () {
    $(function () {
      $("#my_date_picker").datepicker({
        dateFormat: "dd/mm/yy",
        minDate: new Date("1/30/2020"),
        maxDate: "-1D",
        beforeShow: function () {
          $(".ui-datepicker").css("font-size", 12);
          // $(".ui-datepicker").css("height", 12);
        },
      });
    });
  });
});
function GetDemoState() {
  // console.log(e);
  var e = document.getElementById("state-name");
  var state = e.options[e.selectedIndex].text;
  if (state != "All") {
    var p = document.getElementById("district-select");
    var district = p.options[p.selectedIndex].text;

    if (district != "All") {
      var q = document.getElementById("city-select");
      var city = q.options[q.selectedIndex].text;
    }
  }
  var date_data = document.getElementById("my_date_picker").value;
  //   var date = r.options[r.selectedIndex].text;
  //   console.log(date);
  if (district == undefined && date_data == "") {
    var place = state;
    var date = "All";
  } else if (district == undefined && date_data != "") {
    var place = state;
    var date = date_data;
  } else if (city == undefined && date_data != "") {
    var place = state;
    var date = date_data;
  } else if (city == undefined && date_data == "") {
    var place = state;
    var date = "All";
  } else if (city != undefined && date_data != "") {
    if (city === "All") {
      var place = district;
    } else {
      var place = city;
    }
    var date = date_data;
  } else if (city != undefined && date_data == "") {
    if (city === "All") {
      var place = district;
    } else {
      var place = city;
    }
    var date = "All";
  }
  console.log(place);
  console.log(date);
  $.post(
    "/Demography",
    {
      place_data: place,
      date_day: date,
    },
    function (data, status, xhr) {
      var df = data;
      console.log(df);
      if (df != "None") {
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
        //   console.log(JSON.parse(data));
        //   console.log(Object.values(df[0]));
        divShowData.innerHTML = "";
        divShowData.appendChild(table);
        divShowData.style.width = "auto";
        // divShowData.style.background = "grey";
        divShowData.style.overflow = "auto";
        divShowData.style.marginTop = "20px";
      } else if (df == "None") {
        var divShowData = document.getElementById("data_show");
        divShowData.innerHTML = "<h2>No Data Found for " + date + "</h2";
        // divShowData.style.color = "red";
        divShowData.style.marginTop = "10px";
      }
    }
  );

  //   console.log(result);
  // document.getElementById("result").innerHTML = result;
}
