var Player = React.createClass({
	render: function(){
		return (
			<div>
				<h4>player object</h4>
				<div>
					<h5>hand</h5>
					<Hand cards = {this.props.player.hand} />
				</div>
			</div>
		)
	}
});

