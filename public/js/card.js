var Card = React.createClass({
	render : function(){
		return (
			<span>
				<img className = "card" src={this.props.card.images.low_resolution.url} />
			</span>
		)
	},
	componentDidMount: function(){
		console.log(this.props.card)
	}
})