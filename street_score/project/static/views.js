var StreetScore = StreetScore || {};

(function(S) {
  S.StreetView = Backbone.View.extend({
    initialize: function() {
      // Init Google Street View
      this.sv = new google.maps.StreetViewService();
      this.pano =  new google.maps.StreetViewPanorama(document.getElementById('streetview-container'));

      // Bind model change event
      this.model.bind('change', this.render, this);
    },

    render: function() {
      var latLng = new google.maps.LatLng(this.model.get('point').lat, this.model.get('point').lon);
      var view = this;

      this.sv.getPanoramaByLocation(latLng, 50, function(data, status){
        view.pano.setPano(data.location.pano);
        view.pano.setPov({
          heading: 270,
          pitch: 0,
          zoom: 1
        });
        view.pano.setVisible(true);
      });
    }
  });

  S.RatingsView = Backbone.View.extend({
    initialize: function() {
      this.$container = $('.well');

      // Bind model change event
      this.model.bind('change', this.render, this);
    },
    render: function() {
      var template = Mustache.template('ratings'),
        questions = this.model.get('questions'),
        ratings = [];

      _.each(questions, function(obj, i){
        ratings.push({
          'criterion': obj.id,
          'question': obj.prompt,
          'score': 0
        });
      });

      var html = template.render({ 'ratings': ratings });
      console.log(this.$container);
      console.log(html);

      this.$container.html(html);
    }
  });

  S.AppView = Backbone.View.extend({
    initialize: function() {
      var model = new S.SurveySessionModel(),
          streetView = new StreetScore.StreetView({ model: model }),
          ratingsView = new StreetScore.RatingsView({ model: model });

      model.fetch();
    }
  });
})(StreetScore);

var app = new StreetScore.AppView();