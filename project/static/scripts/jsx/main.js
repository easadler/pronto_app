/** @jsx React.DOM */
var SetIntervalMixin = {
  componentWillMount: function() {
    this.intervals = [];
  },
  setInterval: function() {
    this.intervals.push(setInterval.apply(null, arguments));
  },
  componentWillUnmount: function() {
    this.intervals.map(clearInterval);
  }
};

var Circle = React.createClass({
    mixins: [SetIntervalMixin], 
    getDefaultProps: function() {
        return {
            r: 0,
            fill: 'green',
            cx: 0,
            cy: 0,
            opacity: 0.6
        }
    },
    
    getInitialState: function() {
      return {
        milliseconds: 0,
        r: 0
      };
    },
    
    shouldComponentUpdate: function(nextProps) {
      return this.props.r !== this.state.r;
    },
    
    componentWillMount: function() {
      console.log('will mount');
    },
    
    componentWillReceiveProps: function(nextProps) {
      this.setState({milliseconds: 0, r: this.props.r});
    this.setState({fill: this.props.fill});

    },
    
    componentDidMount: function() {
      this.setInterval(this.tick, 10);
    },
    
    tick: function(start) {
      this.setState({milliseconds: this.state.milliseconds + 10});
    },
    
    render: function() {
      var easyeasy = d3.ease('back-out');
      var r = this.state.r + (this.props.r - this.state.r) * easyeasy(Math.min(1, this.state.milliseconds/1000));

      var fill = this.state.fill
        return (
      <circle
                cx = {this.props.cx}
                cy = {this.props.cy}
                r =  {r}
                fill = {'green'}
                opacity = {this.props.opacity}>
           </circle>
        );
    },
});

var Path = React.createClass({ 
    render: function() {
      var d = this.props.d
        return (
      <path
                d = {d}
                fill = {'black'}>
           </path>
        );
    },
});

var Hood = React.createClass({
  getDefaultProps: function() {
    return {
      hoods: []
    }
  },

  shouldComponentUpdate: function(nextProps) {
      return this.props.hoods !== nextProps.hoods;
  },

  render: function() {
    var hoods = this.props.hoods;

    var pathGenerator = this.props.pathGenerator;

    var paths = hoods.map(function(hood,i) {
      return (
  <Path
     d = {pathGenerator(hood)}
      key = {i}/>
      )
    });

    return (
          <g>{paths}</g>
    );
  }
}); 


var Terminal = React.createClass({
  getDefaultProps: function() {
    return {
      terminals: []
    }
  },

  shouldComponentUpdate: function(nextProps) {
      return this.props.terminals !== nextProps.terminals;
  },

  render: function() {
    var terminals = this.props.terminals;
    var projection = this.props.projection;

    var circles = terminals.map(function(terminal, i) {
      var fill = 'green';
      var size = +terminal.bikes_avail
      var coord = [+terminal.long,+terminal.lat]
      return (
  <Circle
      cx = {projection(coord)[0]}
      cy = {projection(coord)[1]}
      r =  {size}
      fill = {fill}
      opacity = {0.6}
      key = {terminal.terminal}/>
      )
    });

    return (
          <g>{circles}</g>
    );
  }
}); 



var Map = React.createClass({
    render: function() {
        return (
            <svg width={this.props.width} 
                 height={this.props.height} >
              {this.props.children}
            </svg>
        );
    }
});


App = React.createClass({
  getDefaultProps: function() {
    return {
      width: 960,
      height: 700
    };
  },

  getInitialState: function() {
    return {
      hoods: [],
      terminals: [],
    };
  },

  componentWillMount: function() {
    var cmp = this;
        var hoods = '{{hoods|safe}}';
        cmp.setProps({
          hoods: topojson.feature(hoods,hoods.objects.Seattle).features
        });
        cmp.setState({
          terminals: '{{terminals|safe}}'
        });
  },


  render: function() {
    var cmp = this;

    var svg = React.DOM.svg;

  var projection = d3.geo.albers()
      .scale( 450000 )
      .rotate( [122.335167,0] )
      .center( [0, 47.608013] )
      .translate( [590/2,1000/2] );

    var counties = this.state.counties
    var terminals = this.state.terminals

    var pathGenerator = d3.geo.path().projection(projection);

    return (<Map  width={this.props.width} 
                  height= {this.props.height}>
              <Hood hoods = {this.props.hoods} pathGenerator = {pathGenerator}/>
              <Terminal terminals = {this.state.terminals}
                projection = {projection}/>
            </Map>);
}

});

React.render(
  <App />,
  document.getElementById('main'));