var StreetScore = StreetScore || {};

(function(S) {
  S.StreetviewView = Backbone.View.extend({
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

      this.sv.getPanoramaByLocation(latLng, 75, function(data, status){
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


  S.StreetImageView = Backbone.View.extend({
    initialize: function(options) {

      // The index of the block in the array
      this.index = this.options.index;

      // Bind model change event
      this.model.bind('change', this.render, this);
    },

    render: function() {
      var block = this.model.get('blocks')[this.index],
          self = this;

      $(this.el).html('<img src="http://maps.googleapis.com/maps/api/streetview?size=600x600&location='+block.point.lat+','+block.point.lon+'&heading=0&fov=90&pitch=5&sensor=false" />');
    },

    stopRotation: function() {
      //noop
    }
  });

  /**
   * The view class for a list of ratings.
   */
  S.RatingsView = Backbone.View.extend({
    el: '#ratings-container',

    initialize: function() {
      // Bind model change event
      this.model.bind('change', this.render, this);
    },

    render: function() {
      var questions = [this.model.get('questions')[0]],
          blocks = this.model.get('blocks'),
          ratings = new S.RatingCollection(),
          self = this;

      // Empty the list before appending
      $(this.el).empty();

      // As we add new ratings to the collection, we want new views to be
      // associated with them.
      ratings.bind('add', function(rating) {
        self.ratingView = new S.RatingView({ model: rating });
        $(self.ratingView.render().el).children().appendTo(self.el);
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
    },

    events : {
      'click .btn' : 'setScore'
    },

    setScore: function(e) {
      var newScore = $(e.currentTarget).attr('data-score');
      this.ratingView.setScore(newScore);
      S.app.next();
    }

  });

  /**
   * The view class for a single rating model.  Constructed as a sub-view of
   * a RatingsView.
   */
  S.RatingView = Backbone.View.extend({
    initialize: function() {
      this.model.bind('change', this.render, this);
    },

    render: function() {
      var template = Mustache.template('rating'),
          rating = this.model,
          html = template.render(rating.toJSON());

      // Set the question text
      $('#question span').text(this.model.get('question'));

      $(this.el).html(html);
      return this;
    },

    setScore: function(score) {
      this.model.save({'score': score});
    }

  });

  S.AppView = Backbone.View.extend({
    el: 'body',

    initialize: function() {
      this.model = new S.SurveySessionModel();
      this.streetView1 = new StreetScore.StreetviewView({ model: this.model, index: 0, el: '#streetview-container1' });
      this.streetView2 = new StreetScore.StreetviewView({ model: this.model, index: 1, el: '#streetview-container2' });
      this.ratingsView = new StreetScore.RatingsView({ model: this.model });

      this.next();
    },

    events: {
      "click a#next-survey": "next"
    },

    next: function() {
      this.streetView1.stopRotation();
      this.streetView2.stopRotation();
      this.model.fetch();
    }
  });
})(StreetScore);

StreetScore.app = new StreetScore.AppView();
