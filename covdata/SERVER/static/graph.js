$(document).ready(function () {
  $("li:eq(4)").addClass("active");
});
function GetGraphData() {
  // $("canvas#graph").remove();
  if (window.myChart) window.myChart.destroy();
  var e = document.getElementById("graph-state");
  var state_name = e.options[e.selectedIndex].text;
  var p = document.getElementById("daily");
  var daily = p.options[p.selectedIndex].text;
  var q = document.getElementById("cond-id");
  var condition = q.options[q.selectedIndex].text;
  if (daily === "Yes") {
    var q = "Daily";
  } else {
    var q = "Cumulative";
  }
  $.post(
    "/Graph",
    {
      state_data: JSON.stringify(state_name),
      daily_data: JSON.stringify(daily),
      condition_data: JSON.stringify(condition),
    },
    function (data, status, xhr) {
      // $("div#chart").append(
      //   '<canvas id="graph" width="600" height="200"></canvas>'
      // );
      var ctx = document.getElementById("graph").getContext("2d");
      if (condition != "Together") {
        // console.log(myChart);

        window.myChart = new Chart(ctx, {
          type: "line",
          data: {
            labels: Object.keys(data[0]).slice(1),
            datasets: [
              {
                label: state_name + " " + q + " Count cases " + condition,
                data: Object.values(data[data.length - 1]).slice(1),
                backgroundColor: [
                  "rgba(255, 50, 50, 1)",
                  // "rgba(54, 162, 235, 0.2)",
                  // "rgba(255, 206, 86, 0.2)",
                  // "rgba(75, 192, 192, 0.2)",
                  // "rgba(153, 102, 255, 0.2)",
                  // "rgba(255, 159, 64, 0.2)",
                ],
                borderColor: [
                  "rgba(255, 0, 0, 1)",
                  // "rgba(54, 162, 235, 1)",
                  // "rgba(255, 206, 86, 1)",
                  // "rgba(75, 192, 192, 1)",
                  // "rgba(153, 102, 255, 1)",
                  // "rgba(255, 159, 64, 1)",
                ],
                fill: false,
                borderWidth: 1,
              },
            ],
          },
          options: {
            animation: {
              duration: 2000,
            },
            scales: {
              yAxes: [
                {
                  ticks: {
                    beginAtZero: true,
                  },
                },
              ],
            },
          },
        });
      } else {
        // var df_1 = JSON.parse(data[0]);
        // var df_2 = JSON.parse(data[1]);
        // var df_3 = JSON.parse(data[2]);
        var cond = ["confirmed", "recovered", "deceased"];
        var color = [
          "rgba(255, 0, 0, 1)",
          "rgba(0, 255, 0, 1)",
          "rgba(0, 0, 255, 1)",
        ];
        var dataset = [];
        for (i = 0; i < data.length; i++) {
          var label = state_name + " " + q + " Count cases for " + cond[i];
          var d = Object.values(
            JSON.parse(data[i])[JSON.parse(data[i]).length - 1]
          ).slice(1);
          var back_color = ["rgba(255, 99, 132, 0.2)"];
          var border = color[i];
          dataset.push({
            label: label,
            data: d,
            backgroundColor: back_color,
            borderColor: border,
            fill: false,
            borderWidth: 1,
          });
        }
        window.myChart = new Chart(ctx, {
          type: "line",
          animationEasing: "linear",
          data: {
            labels: Object.keys(JSON.parse(data[0])[0]).slice(1),
            datasets: dataset,
          },
          options: {
            scales: {
              yAxes: [
                {
                  ticks: {
                    beginAtZero: true,
                  },
                },
              ],
            },
            tooltips: {
              mode: "x",
            },
          },
        });
      }
    }
  );
}
