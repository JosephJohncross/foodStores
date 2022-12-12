anychart.onDocumentReady(function () {

    var lineDarkTheme = {
        "background": {
            "fill": "#000"
        }
    }

    anychart.theme([lineDarkTheme])
    // create data set on our data
    var dataSet = anychart.data.set(getData());

    // map data for the first series, take x from the zero column and value from the first column of data set
    var firstSeriesData = dataSet.mapAs({ x: 0, value: 1 });

    // map data for the third series, take x from the zero column and value from the third column of data set
    var thirdSeriesData = dataSet.mapAs({ x: 0, value: 3 });

    // create line chart
    var chart = anychart.line();

    // turn on chart animation
    chart.animation(true);

    // set chart padding
    chart.padding([10, 20, 25, 20]);

    // turn on the crosshair
    chart.crosshair().enabled(true).yLabel(false).yStroke(null);

    // set tooltip mode to point
    chart.tooltip().positionMode('point');
    
    // set chart title text settings
    var title = chart.title()
    title.enabled(true);
    title.text('Revenue')
    title.width(800);
    title.textSettings('fontColor', '#000');
    title.textSettings('fontSize', '18px');


    // set yAxis title
    // chart.yAxis().title('Number of Bottles Sold (thousands)');
    chart.xAxis().labels().padding(5);

    chart.xScale().mode('continuous');

    // create first series with mapped data
    var firstSeries = chart.line(firstSeriesData);
    firstSeries.name('Income');
    firstSeries.hovered().markers().enabled(true).type('circle').size(4);
    firstSeries
      .tooltip()
      .position('right')
      .anchor('left-center')
      .offsetX(5)
      .offsetY(5);

    // create third series with mapped data
    var thirdSeries = chart.line(thirdSeriesData);
    thirdSeries.name('Expenses');
    thirdSeries.hovered().markers().enabled(true).type('circle').size(4);
    thirdSeries
      .tooltip()
      .position('right')
      .anchor('left-center')
      .offsetX(5)
      .offsetY(5);
      thirdSeries.color('#fa8e29');

    // turn the legend on
    chart.legend().enabled(true).fontSize(13).padding([0, 0, 0, 0]);

    // set container id for the chart
    chart.container('container');
    // initiate chart drawing
    chart.draw();
    

    // Chart Two
    var data = anychart.data.set([
        ["Jun 24", 123, 5, "#a1e5af", "#82b0e3", null, {enabled: true}],
        ["Jun 25", 15, 12, "#a1e5af", "#82b0e3", null, {enabled: true}],
        ["Jun 26", 130, 86, "#a1e5af", "#82b0e3", null, {enabled: true}],
        ["Jun 27", 18, 26, "#a1e5af", "#82b0e3", null, {enabled: true}],
        ["Jun 28", 90, 110, "#a1e5af", "#82b0e3", null, {enabled: true}]
      ]);
      
      // map the data
      var seriesData_1 = data.mapAs({x: 0, value: 1, fill: 3, stroke: 5, label: "Test"});
      var seriesData_2 = data.mapAs({x: 0, value: 2, fill: 4, stroke: 5, label: "Note"});
    //   seriesData_1.title("Test")
      // create a chart
      var barChart = anychart.bar();
    //   barChart.title("Order ")
      var title2 = barChart.title();
      title2.enabled(true)
      title2.text("Order Summary")
      title2.textSettings('fontColor', '#000');
      title2.textSettings('fontSize', '18px');
      
      barChart.yAxis().labels().rotation(-90);
      var series1 = barChart.bar(seriesData_1);
      var series2 = barChart.bar(seriesData_2);

      barChart.container('barChart');

      // initiate chart drawing
      barChart.draw();
});

  function getData() {
    return [
      ['Jan', 3.6, 2.3, 2.8, 11.5],
      ['Feb', 7.1, 4.0, 4.1, 14.1],
      ['Mar', 8.5, 6.2, 5.1, 17.5],
      ['Apr', 9.2, 11.8, 6.5, 18.9],
      ['May', 10.1, 13.0, 12.5, 20.8],
      ['Jun', 11.6, 13.9, 18.0, 22.9],
      ['July', 16.4, 18.0, 21.0, 25.2],
      ['Aug', 18.0, 23.3, 20.3, 27.0],
      ['Sep', 13.2, 24.7, 19.2, 26.5],
      ['Oct', 12.0, 18.0, 14.4, 25.3],
      ['Nov', 3.2, 15.1, 9.2, 23.4],
      ['Dec', 4.1, 11.3, 5.9, 19.5]
    ];
  }