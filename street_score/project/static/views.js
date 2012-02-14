var StreetScore = StreetScore || {};

(function(S) {
  S.sv = new google.maps.StreetViewService();

  // View to render a full Street View panel
  S.StreetviewView = Backbone.View.extend({
    className: 'streetview',

    initialize: function() {
      var self = this,
          heading = 0;

      // Init the panoramo object
      self.pano =  new google.maps.StreetViewPanorama(this.el, {
        linksControl: false,
        addressControl: false,
        zoomControlOptions: {
          style: google.maps.ZoomControlStyle.SMALL
        }
      });
    },

    render: function(success, error) {
      var self = this,
          latLng = new google.maps.LatLng(self.options.point.lat, self.options.point.lon);

      // Check for street view imagery, 50m radius
      S.sv.getPanoramaByLocation(latLng, 50, function(data, status) {
        if (status === google.maps.StreetViewStatus.OK) {
          // Setup the panorama
          self.pano.setPano(data.location.pano);
          self.pano.setPov({
            heading: 0,
            pitch: 5,
            zoom: 1
          });
          self.pano.setVisible(false);

          if (success) {success(self.el);}
        } else {
          if (error) { error(); }
        }
      });
    },

    events : {
      'mousedown' : 'stopRotation'
    },

    show: function() {
      var self = this,
          heading = 0;

      // Make the panorama visible
      self.pano.setVisible(true);

      // http://stackoverflow.com/questions/6809573/google-street-view-problem-javascript
      google.maps.event.trigger(self.pano, 'resize');

      if (self.options.rotate) {
        self.rotate_id = setInterval(function(){
          self.pano.setPov({
            heading: heading+=0.5,
            pitch: 5,
            zoom: 1
          });
        }, 40);
      }
    },

    stopRotation: function() {
      // Stop rotating street view on mousedown
      if (this.rotate_id) {
        clearInterval(this.rotate_id);
      }
    }
  });

  // Static street view images
  S.StreetImageView = Backbone.View.extend({
    tagName: 'img',
    className: 'streetview',

    render: function(success, error) {
      var self = this,
          latLng = new google.maps.LatLng(self.options.point.lat, self.options.point.lon);

      // Check for street view imagery, 50m radius
      S.sv.getPanoramaByLocation(latLng, 50, function(data, status) {
        if (status === google.maps.StreetViewStatus.OK) {
          if (success) { success(self.el); }
        } else {
          if (error) { error(); }
        }
      });
    },

    show: function(){
      var self = this,
          url = 'http://maps.googleapis.com/maps/api/streetview?size=550x550&location='+
          self.options.point.lat+','+self.options.point.lon+'&heading=0&fov=90&pitch=5&sensor=false';

      $(self.el).attr('src', url);
    }
  });

  // View for an entire survey, including two SVs to compare
  S.SurveyView = Backbone.View.extend({
    // Bootstrap carousels want this class
    className: 'item',

    initialize: function() {
      var self = this;

      // When a survey is shown, so the SV views
      $(document).on('show', function(e) {
        if (self.sv1.stopRotation) {self.sv1.stopRotation();}
        if (self.sv2.stopRotation) {self.sv2.stopRotation();}

        if ($(self.el).is('.active')) {
          // Remove previous surveys from the DOM
          $(self.el).prevAll().remove();

          self.sv1.show();
          self.sv2.show();
        }
      });
    },

    render: function(success, error) {
      var self = this;
      self.sv1 = new S.StreetviewView({point: this.options.point1, rotate: false});
      self.sv2 = new S.StreetviewView({point: this.options.point2, rotate: false});

      // Attempt to render street view 1, success or
      self.sv1.render(function(el1){
        self.sv2.render(function(el2){
          // Both points have street view, so render...
          var template = Mustache.template('survey');
          $(self.el).html(template.render(self.model.toJSON()));

          // Append street views
          $('.first.survey-choice', self.el).append(el1);
          $('.second.survey-choice', self.el).append(el2);

          if (success) {success(self.el);}
        }, function(){
          if (error) {error();}
        });
      }, function(){
        if (error) {error();}
      });
    },

    events : {
      'click .vote' : 'vote'
    },

    vote: function(e) {
      // Record a score and go the next survey
      var newScore = $(e.currentTarget).attr('data-score');
      this.model.save({'score': newScore});
      $(document).trigger('next');
    }
  });

  // The view for the app, of course
  S.AppView = Backbone.View.extend({
    el: '#survey-container',

    initialize: function() {
      var self = this,
          QUEUE_SIZE = 4;

      self.model = new S.SurveySessionCollection();

      // Render thyself when the surveys show up
      self.model.bind('reset', self.render, self);

      // Tells the carousel to advance ot the next survey
      // and fetch more surveys from the server.
      $(document).on('next', function(){
        $('.carousel').carousel('next');

        // Only fetch surveys the total number of surveys we need
        var surveysToFetch = QUEUE_SIZE - $('.item:not(.active)').length;
        // console.log('fetching ' + surveysToFetch + ' surveys.');
        if (surveysToFetch) {
          self.model.fetch({ data: {count:surveysToFetch} });
        }
      });

      // Trigger a more generica 'show' event when the carousel
      // advances to the next survey. The surveys sometimes need
      // to do something.
      $(document).on('slid', '.carousel', function(){
        $(document).triggerHandler('show');
      });

      // Skip the current survey on link click
      $(document).on('click', '#skip', function() {
        $(document).trigger('next');
      });

      // Fetch the first batch of surveys
      this.model.fetch({ data: {count:QUEUE_SIZE} });

      // Init the carousel widget.
      $('.carousel').carousel({interval: 3600000});
    },

    render: function() {
      var self = this;

      // Turn each survey model into a rating model so we can
      // rate each street view.
      this.model.each(function(surveyModel) {
        var question = surveyModel.get('questions')[0],
            blocks = surveyModel.get('blocks'),
            ratingModel = new S.RatingModel({
              'criterion': question.id,
              'question': question.prompt,
              'score': 0,
              'segment1': blocks[0].segment_id,
              'block1_index': blocks[0].block_index,
              'segment2': blocks[1].segment_id,
              'block2_index': blocks[1].block_index
            }),
            // Make the survey, not yet rendered
            view = new S.SurveyView( {
              model: ratingModel,
              point1: surveyModel.get('blocks')[0].point,
              point2: surveyModel.get('blocks')[1].point
            });

        // Render the survey view...
        view.render(function(el) {
          // ...then append it to the DOM on the callback
          $(self.el).append(el);

          // Make sure an item is active to make the carousel happy
          if ($('.item', self.el).hasClass('active') === false) {
            $('.item:first', self.el).addClass('active');
            // First time, make sure show is triggered
            setTimeout(function(){$(document).triggerHandler('show');},200);
          }
        });
      });
    }
  });
})(StreetScore);

$(document).ready(function() {
  StreetScore.app = new StreetScore.AppView();
});