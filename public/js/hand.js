var Hand = React.createClass({
	render: function(){

		var cards = this.props.cards.map(function(card){
			return <Card card={card} />;
		})
		return (
			<div>
				<h3>Cards</h3>
				{cards}
			</div>
		)
	}
})