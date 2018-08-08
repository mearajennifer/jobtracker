"use strict";

// Javascript to render profile page info, profile editing

// Parent container -- Profile
class UserProfile extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <React.Fragment>
                <UserGreeting />
                <UserName fname={this.props.fname} lname={this.props.lname} />
            </React.Fragment>
            )
    }
}

// User name component
class UserName extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <p>{this.props.fname} {this.props.lname}</p>
        );
    }
}


// Greeting component
class UserGreeting extends React.Component {
    constructor(props) {
        super(props);
        this.state = { value: 'Hello, world!' };
    }

    greet = () => {
        const greeting_list = ['Hello, world!', 'You\'ve got this!', 'Today\'s your day!', 'Dream it. Do it.', 'Work hard. Dream big.', 'Prove them wrong.', 'You can and you will.'];
        const greeting = greeting_list[Math.floor(Math.random() * greeting_list.length)];
        this.setState({ value: greeting })
    }

    render() {
        return (
            <h5 className="greeting" onClick={this.greet}>
                {this.state.value}
            </h5>
        );
    }
}


// render Parent
ReactDOM.render(
    <UserProfile />,
    document.getElementById('profile-info')
);
