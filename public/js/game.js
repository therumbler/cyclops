var Game = React.createClass({
	getInitialState: function(){
		return {
			"game": false
		}
	},
	render: function(){
		var hand = false;
		if(this.state.game){
			hand = <Hand cards =  {this.state.game.game.player.hand} />;
		}
		return (
			<div className = "game">
			{hand}
			</div>
		)
	},
	parseResponse: function(response){
		this.setState({"game": response});
	},
	load: function(){
		var url = "api/games/" + this.props.gameId + "?token=" + this.props.token;
		get(url, this.parseResponse);
	},
	componentDidMount: function(){
		console.log("mounted");
		this.load();
	}
});

var querySring = getQueryString()
var gameId = querySring["id"];

console.log(gameId);
var token = "54206.abc123";

React.render(
	<Game gameId = {gameId} token = {token}/>,
	document.getElementById("game")
);