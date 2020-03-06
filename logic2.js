///////use this/////
function buildCharts(sample) {
  d3.json("/artists").then((data) => {
    var resultArray = data.filter(sampleObj => sampleObj.artist == sample);
    var song = resultArray.map(row => row.title)
    var length = resultArray.map(row => row.issue_date.length)
    var layout = { title: `${sample}'s Hit Songs and Number of Weeks at #1`,margin: { t: 50, b: 200 } };
    console.log(resultArray)
    console.log(length)
    var data = [
      {
        x: song,
        y: length,
        type: "bar",
      
      }
    ];
    
    Plotly.newPlot("Chart3", data, layout);
    
    ////Group songs based on title to remove the duplicates
    var output = [];

    resultArray.forEach(function(item) {
      var existing = output.filter(function(v, i) {
        return v.title == item.title;
      });
      if (existing.length) {
        var existingIndex = output.indexOf(existing[0]);
        output[existingIndex].issue_date = output[existingIndex].issue_date.concat(item.issue_date);
      } else {
        if (typeof item.issue_date == 'string')
          item.issue_date = [item.issue_date];
        output.push(item);
      }
    });
    



    
    var layout2 = { title: `${sample}'s Hit Songs Over Time`,margin: { t: 50, b: 200 } };
    var desired_maximum_marker_size = 40;   
    var length2 = output.map(row => row.issue_date.length)
    var size = length2;
    var year2 = output.map(row => row.year);
    var data2 = [
      {
        x: year2,
        y: length2,
        mode: "markers",
        marker: {
          size: size,
          sizeref: 2.0 * Math.max(...size) / (desired_maximum_marker_size**2),
          sizemode: 'area'
      }}];
    
    Plotly.newPlot("Chart4", data2, layout2);

    
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selArtist");
  
  // Use the list of sample names to populate the select options
  d3.json("/artists").then((data) => {
    var sampleNames = [...new Set(data.map(row => row.artist))].sort();

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
