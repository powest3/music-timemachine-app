///////use this/////


function buildCharts(sample) {
  d3.json("/alldata").then((data) => {
    var resultArray = data.filter(sampleObj => sampleObj.decade == sample);
    var topValues = resultArray.sort((a,b) => b.issue_date.length-a.issue_date.length).slice(0,10);
    var song = topValues.map(row => row.title)
    var vader = topValues.map(row => row.VADER)
    var layout = {barmode: 'relative'};
    // { title: `${sample}'s Hit Songs and Number of Weeks at #1`,margin: { t: 50, b: 200 } };
    var data = [
      {
        x: song,
        y: vader,
        type: "bar",
      
      }
    ];
    Plotly.newPlot('WordChart', data, layout);


    var counts = resultArray.reduce((c, { sentiment: key }) => (c[key] = (c[key] || 0) + 1, c), {});

    console.log(counts);
    var data = [{
      type: "pie",
      values: Object.values(counts),
      labels: Object.keys(counts),
      textinfo: "label+percent",
      insidetextorientation: "radial"
    }]
    
    var layout = [{
      height: 700,
      width: 700
    }]
    
    Plotly.newPlot('BarChart', data, layout)
    
    // ////Group songs based on title to remove the duplicates
    // var output = [];

    // resultArray.forEach(function(item) {
    //   var existing = output.filter(function(v, i) {
    //     return v.title == item.title;
    //   });
    //   if (existing.length) {
    //     var existingIndex = output.indexOf(existing[0]);
    //     output[existingIndex].issue_date = output[existingIndex].issue_date.concat(item.issue_date);
    //   } else {
    //     if (typeof item.issue_date == 'string')
    //       item.issue_date = [item.issue_date];
    //     output.push(item);
    //   }
    // });
    



    
    // var layout2 = { title: `${sample}'s Hit Songs Over Time`,margin: { t: 50, b: 200 } };
    // var desired_maximum_marker_size = 40;   
    // var length2 = output.map(row => row.issue_date.length)
    // var size = length2;
    // var year2 = output.map(row => row.year);
    // var data2 = [
    //   {
    //     x: year2,
    //     y: length2,
    //     mode: "markers",
    //     marker: {
    //       size: size,
    //       sizeref: 2.0 * Math.max(...size) / (desired_maximum_marker_size**2),
    //       sizemode: 'area'
    //   }}];
    
    // Plotly.newPlot("BarChart", data2, layout2);

    
  });
}

// var changedElement = d3.select(".vertical-menu").on("click");
// var elementValue = changedElement.property("value");
// var element = attr("id").on("click",buildCharts);
// d3.select("#id").on("click",buildCharts);

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selArtist");
  
  // Use the list of sample names to populate the select options
  d3.json("/alldata").then((data) => {
    var output = [];

    data.forEach(function(item) {
      var existing = output.filter(function(v, i) {
        return v.artist == item.artist;
      });
      if (existing.length) {
        var existingIndex = output.indexOf(existing[0]);
        output[existingIndex].title = output[existingIndex].title.concat(item.title);
      } else {
        if (typeof item.title == 'string')
          item.title = [item.title];
        output.push(item);
      }
    });
    console.log(output)
 var resultArray2 = output.map(row => row.decade)
 var sampleNames = [...new Set(resultArray2)];
    
    // var resultArray2 = data.filter(sampleObj => sampleObj.issue_date.length >2);
    // var sampleNames = [...new Set(data.map(row => row.artist))].sort();

    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    var firstSample = sampleNames[0];
    buildCharts(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
}

// Initialize the dashboard
init();
