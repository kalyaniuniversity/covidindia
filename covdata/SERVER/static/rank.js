$(document).ready(function () {
  $("li:eq(3)").addClass("active");
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
  $("#my_date_picker").change(function () {
    var el = $(this);
    if (el.val() != "" && $("#condition").val() == "Cumulative") {
      $("#selection-section select:last-child").remove();
    } else if (el.val() == "" && $("#condition").val() != "Cumulative") {
      $("#selection-section").append(
        '<span><select id="state-name"><option value="All">--select state--</option><option value="West Bengal">West Bengal</option><option value="Uttarakhand">Uttarakhand</option><option value="Uttar Pradesh">Uttar Pradesh</option><option value="Tripura">Tripura</option><option value="Telangana">Telangana</option><option value="Tamil Nadu">Tamil Nadu</option><option value="Rajasthan">Rajasthan</option><option value="Punjab">Punjab</option><option value="Puducherry">Puducherry</option><option value="Odisha">Odisha</option><option value="Mizoram">Mizoram</option><option value="Meghalaya">Meghalaya</option><option value="Manipur">Manipur</option><option value="Maharashtra">Maharashtra</option><option value="Madhya Pradesh">Madhya Pradesh</option><option value="Ladakh">Ladakh</option><option value="Kerala">Kerala</option><option value="Karnataka">Karnataka</option><option value="Jharkhand">Jharkhand</option><option value="Jammu and Kashmir">Jammu and Kashmir</option><option value="Himachal Pradesh">Himachal Pradesh</option><option value="Haryana">Haryana</option><option value="Gujarat">Gujarat</option><option value="Goa">Goa</option><option value="Delhi">Delhi</option><option value="Chhattisgarh">Chhattisgarh</option><option value="Chandigarh">Chandigarh</option><option value="Bihar">Bihar</option><option value="Assam">Assam</option><option value="Arunachal Pradesh">Arunachal Pradesh</option><option value="Andhra Pradesh">Andhra Pradesh</option><option value="Andaman and Nicobar Islands">Andaman and Nicobar Islands</option></select></span>'
      );
    } else if (el.val() != "" && $("#condition").val() != "Cumulative") {
      $("#selection-section select:last-child").remove();
    }
  });
  $("#condition").change(function () {
    var el = $(this);
    if (el.val() != "Daily") {
      $("#selection-section select:last-child").remove();
    } else if (el.val() == "Daily" && $("#my_date_picker").val() == "") {
      $("#selection-section").append(
        '<span><select id="state-name"><option value="All">--select state--</option><option value="West Bengal">West Bengal</option><option value="Uttarakhand">Uttarakhand</option><option value="Uttar Pradesh">Uttar Pradesh</option><option value="Tripura">Tripura</option><option value="Telangana">Telangana</option><option value="Tamil Nadu">Tamil Nadu</option><option value="Rajasthan">Rajasthan</option><option value="Punjab">Punjab</option><option value="Puducherry">Puducherry</option><option value="Odisha">Odisha</option><option value="Mizoram">Mizoram</option><option value="Meghalaya">Meghalaya</option><option value="Manipur">Manipur</option><option value="Maharashtra">Maharashtra</option><option value="Madhya Pradesh">Madhya Pradesh</option><option value="Ladakh">Ladakh</option><option value="Kerala">Kerala</option><option value="Karnataka">Karnataka</option><option value="Jharkhand">Jharkhand</option><option value="Jammu and Kashmir">Jammu and Kashmir</option><option value="Himachal Pradesh">Himachal Pradesh</option><option value="Haryana">Haryana</option><option value="Gujarat">Gujarat</option><option value="Goa">Goa</option><option value="Delhi">Delhi</option><option value="Chhattisgarh">Chhattisgarh</option><option value="Chandigarh">Chandigarh</option><option value="Bihar">Bihar</option><option value="Assam">Assam</option><option value="Arunachal Pradesh">Arunachal Pradesh</option><option value="Andhra Pradesh">Andhra Pradesh</option><option value="Andaman and Nicobar Islands">Andaman and Nicobar Islands</option></select></span>'
      );
    }
  });
});
function GetRankData() {
  var e = document.getElementById("kind");
  var kind = e.options[e.selectedIndex].text;
  var number = document.getElementById("Number").value;

  var p = document.getElementById("by");
  var by = p.options[p.selectedIndex].text;

  var q = document.getElementById("condition");
  var condition = q.options[q.selectedIndex].text;
  var date = document.getElementById("my_date_picker").value;
  if (date == "" && condition == "Daily") {
    var r = document.getElementById("state-name");
    var state = r.options[r.selectedIndex].text;
  }
  if (condition == "Daily") {
    var cumulative = "False";
  } else {
    var cumulative = "True";
  }
  if (date == "") {
    var date_day = "None";
  } else {
    var date_day = date;
  }
  console.log(kind);
  console.log(number);
  console.log(by);
  console.log(cumulative);
  console.log(date_day);
  console.log(state);

  $.post(
    "/Rank",
    {
      kind_data: kind,
      number_data: number,
      by_data: by,
      cumulative_data: cumulative,
      date_data: date_day,
      state_data: state,
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
      }
    }
  );
}
