var StreetScore = StreetScore || {};

(function(S) {
  S.StreetView = Backbone.View.extend({
    el: '.content',

    initialize: function() {
      // Init Google Street View
      this.sv = new google.maps.StreetViewService();
      this.pano =  new google.maps.StreetViewPanorama(document.getElementById('streetview-container'), {
        linksControl: false,
        zoomControlOptions: {
          style: google.maps.ZoomControlStyle.SMALL
        }
      });

      // Bind model change event
      this.model.bind('change', this.render, this);
    },

    render: function() {
      var latLng = new google.maps.LatLng(this.model.get('point').lat, this.model.get('point').lon),
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
      'mousedown #streetview-container' : 'stopRotation'
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
      this.$container = $('ul#rating-list');

      // Bind model change event
      this.model.bind('change', this.render, this);
    },

    render: function() {
      var questions = this.model.get('questions')
        , ratings = new S.RatingCollection()
        , listView = this;

      // Empty the list before appending
      listView.$container.empty();

      // As we add new ratings to the collection, we want new views to be
      // associated with them.
      ratings.bind('add', function(rating) {
        var itemView = new S.RatingView({model: rating});
        listView.$container.append(itemView.render().el);
      });

      // Loop through the questions, creating a corresponding RatingModel for
      // each.  We add them to the collection instead of just creating them
      // directly because the collection is how they know their URL.
      _.each(questions, function(question){
        ratings.add({
          'criterion': question.id,
          'question': question.prompt,
          'score': 0,
          'segment': listView.model.get('segment_id'),
          'block_index': listView.model.get('block_index')
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
    tagName: 'li',

    initialize: function() {
      this.model.bind('change', this.render, this);
    },

    render: function() {
      var template = Mustache.template('rating')
        , rating = this.model
        , html = template.render(rating.toJSON())
        , view = this;

      $(this.el).html(html);

      $('.star', this.el).raty({
        // HACK: not ideal
        path: '/static/raty',
        hintList: ['bad', 'poor', 'average', 'good', 'great'],
        start: rating.get('score') || 0
      });

      return this;
    },

    events : {
      'click .star' : 'setScore'
    },

    setScore: function() {
      var newScore = this.$('.star').raty('score');
      this.model.save({'score': newScore});
    }
  });

  S.AppView = Backbone.View.extend({
    el: '.well',

    initialize: function() {
      this.model = new S.SurveySessionModel();
      this.streetView = new StreetScore.StreetView({ model: this.model });
      this.ratingsView = new StreetScore.RatingsView({ model: this.model });

      this.fetch();
    },

    events: {
      "click a#next-survey": "fetch"
    },

    fetch: function() {
      this.streetView.stopRotation();
      this.model.fetch();
    }
  });
})(StreetScore);

var app = new StreetScore.AppView();
