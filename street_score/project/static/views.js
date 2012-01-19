var StreetScore = StreetScore || {};

(function(S) {
  S.StreetView = Backbone.View.extend({
    initialize: function() {
      // Init Google Street View
      this.sv = new google.maps.StreetViewService();
      this.pano =  new google.maps.StreetViewPanorama(document.getElementById('streetview-container'));
    },

    render: function() {
      // Do some rendering here
    }
  });
})(StreetScore);

var streetView = new StreetScore.StreetView();