///////use this/////


function buildCharts(sample) {
  d3.json("/alldata").then((data) => {
    var resultArray = data.filter(sampleObj => sampleObj.decade == sample);
    var topValues = resultArray.sort((a,b) => b.issue_date.length-a.issue_date.length).slice(0,10);
    var song = topValues.map(row => row.title)
    var vader = topValues.map(row => row.VADER)
    var layout = {barmode: 'relative', title: `Sentiment Scores for Top 10 Songs from the ${sample}`,margin: { t: 75, b: 150 } };
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
    
    var layout = {title: `Sentiment Scores for all Songs from the ${sample}`,
      height: 400,
      width: 1500
    }
    
    Plotly.newPlot('BarChart', data, layout)
    

    
  });
}

function wordcloud(sample) {
  // // This code works save for later
  $(document).ready(function () {
    // on page load this will fetch data from our flask-app asynchronously
   $.ajax({url: '/wordcloud', success: function (data) {
       // returned data is in string format we have to convert it back into json format
       var words_data = $.parseJSON(data);
       var redwords_data = words_data.filter(sampleObj => sampleObj.decade == sample);
       // we will build a word cloud into our div with id=word_cloud
       // we have to specify width and height of the word_cloud chart
       $('#wordcloud').html("");
       $('#wordcloud').jQCloud(redwords_data, {
           width: 800,
           height: 600
       });
   }});
  });
  }

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
    wordcloud(firstSample)
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  wordcloud(newSample)
}

// Initialize the dashboard
init();


