var StreetScore = StreetScore || {};

(function(S) {
  S.StreetView = Backbone.View.extend({
    initialize: function(options) {
      // Init Google Street View
      this.sv = new google.maps.StreetViewService();
      this.pano =  new google.maps.StreetViewPanorama(this.el, {
        linksControl: false,
        zoomControlOptions: {
          style: google.maps.ZoomControlStyle.SMALL
        }
      });
      this.index = this.options.index;

      // Bind model change event
      this.model.bind('change', this.render, this);
    },

    render: function() {
      var block = this.model.get('blocks')[this.index],
          latLng = new google.maps.LatLng(block.point.lat, block.point.lon),
          heading = 0,
          view = this;

      this.sv.getPanoramaByLocation(latLng, 50, function(data, status){
        if (status === google.maps.StreetViewStatus.OK) {
          view.pano.setPano(data.location.pano);
          view.pano.setVisible(true);

          // Rotate street view automatically by default
          view.rotate_id = setInterval(function(){
            view.pano.setPov({
              heading: heading+=0.5,
              pitch: 5,
              zoom: 1
            });
          }, 40);
        } else {
          // No results, fetch the next segment
          view.model.fetch();
        }
      });
    },

    events : {
      'mousedown' : 'stopRotation'
    },

    stopRotation: function() {
      // Stop rotating street view on mousedown
      clearInterval(this.rotate_id);
    }
  });

  /**
   * The view class for a list of ratings.
   */
  S.RatingsView = Backbone.View.extend({
    initialize: function() {
      // Bind model change event
      this.model.bind('change', this.render, this);
    },

    render: function() {
      var questions = [this.model.get('questions')[0]],
          blocks = this.model.get('blocks'),
          ratings = new S.RatingCollection(),
          self = this;

      // As we add new ratings to the collection, we want new views to be
      // associated with them.
      ratings.bind('add', function(rating) {
        var ratingView = new S.RatingView({
          model: rating,
          el: '#ratings-container',
          onScore: function() { self.model.fetch(); }
        });
      });

      // Loop through the questions, creating a corresponding RatingModel for
      // each.  We add them to the collection instead of just creating them
      // directly because the collection is how they know their URL.
      _.each(questions, function(question){
        ratings.add({
          'criterion': question.id,
          'question': question.prompt,
          'score': 0,
          'segment1': blocks[0].segment_id,
          'block1_index': blocks[0].block_index,
          'segment2': blocks[1].segment_id,
          'block2_index': blocks[1].block_index
        });
      });

      return this;
    }
  });

  /**
   * The view class for a single rating model.  Constructed as a sub-view of
   * a RatingsView.
   */
  S.RatingView = Backbone.View.extend({
    initialize: function() {
      this.model.bind('change', this.render, this);

      this.render();
    },

    render: function() {
      var template = Mustache.template('rating'),
          rating = this.model,
          html = template.render(rating.toJSON());

      $(this.el).html(html);
      return this;
    },

    events : {
      'click .btn' : 'setScore'
    },

    setScore: function(e) {
      var newScore = $(e.currentTarget).attr('data-score');
      this.model.save({'score': newScore});

      // if (this.options.onScore) { this.options.onScore(); }
    }
  });

  S.AppView = Backbone.View.extend({
    el: 'body',

    initialize: function() {
      this.model = new S.SurveySessionModel();
      this.streetView1 = new StreetScore.StreetView({ model: this.model, index: 0, el: '#streetview-container1' });
      this.streetView2 = new StreetScore.StreetView({ model: this.model, index: 1, el: '#streetview-container2' });
      this.ratingsView = new StreetScore.RatingsView({ model: this.model });

      this.fetch();
    },

    events: {
      "click a#next-survey": "fetch"
    },

    fetch: function() {
      this.streetView1.stopRotation();
      this.streetView2.stopRotation();
      this.model.fetch();
    }
  });
})(StreetScore);

var app = new StreetScore.AppView();
