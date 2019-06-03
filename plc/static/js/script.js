      var data = getData()
      var time = new Date()


     Plotly.plot('chart', [
     {
    x:[time],
  y: [data['temp']],
  mode: 'lines',
  marker: {color: 'pink', size: 8},
  line: {width: 4},
  name:'Temperature'
}, {
         x:[data['time']],
  y: [data['humi']],
  mode: 'lines',
  marker: {color: 'gray', size:8},
  line: {width: 4},
  name:'Humidity'
}]);
      var cnt =0;

    var interval = setInterval(function() {
        var data = getData();
        var time = new Date();
     Plotly.extendTraces('chart', {
          x: [[time], [time]],
          y: [[data['temp']], [data['humi']]]
    }, [0, 1])


     cnt = cnt+1;
     console.log(cnt)
 // if(cnt === 100) clearInterval(interval);

}, 1000);



        function getData() {
              var jsonData = new Object();
               $.ajax({
                  url: 'arduino/',
                  datatype: 'json',
                  async: false,
                  type: 'GET',
                  data: "{}",
                  beforeSend: function(XMLHttpRequest){},
                  success: function (data) {
                      jsonData.temp = data['temperature']
                      jsonData.humi = data['humi']
                      jsonData.date = data['date']
                      jsonData.time = data['time']
                  },
                  error: function (request, status, error) {
                      alert("실패")
                  }
              });
               return jsonData
          }