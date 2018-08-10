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
                <UserInformation email={this.props.email} phone={this.props.phone} />
                <UserAnalytics />
            </React.Fragment>
            )
    }
}

// Greeting component
class UserGreeting extends React.Component {
    constructor(props) {
        super(props);
        this.state = { value: firstGreeting };
    }

    greet = () => {
        const newGreeting = greetingList[Math.floor(Math.random() * greetingList.length)];
        this.setState({ value: newGreeting })
    }

    render() {
        return (
            <React.Fragment>
                <div className="row">
                    <h3 className="greeting">{this.state.value}</h3>
                </div>
                <div className="row">
                    <button onClick={this.greet}>Give me another!</button>
                </div>
            </React.Fragment>
        );
    }
}

// User name component
class UserName extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <React.Fragment>
                <div className="row name">
                    <h5>{this.props.fname} {this.props.lname}</h5>
                </div>
            </React.Fragment>
        );
    }
}

// User info component
class UserInformation extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <React.Fragment>
                <div className="row">
                    <p>Email: {this.props.email}</p>
                </div>
                <div className="row ">
                    <p>Phone number: {this.props.phone}</p>
                </div>
            </React.Fragment>
        );
    }
}

// User Analytics
class UserAnalytics extends React.Component {
    constructor(props) {
        super(props);
    }

    // Need to pass JSON from db/server with stats back to this child element

    render() {
        return (
            <React.Fragment>
                <h5>Your latest job tracking stats:</h5>
                
                <div className="row">

                    <div className="card col-2">
                        <div className="card-header">
                            <h5 className="card-title">Interested</h5>
                        </div>
                        <div className="card-body">
                            <h1>{data.interested}</h1>
                        </div>
                    </div>
                    <div className="card col-2">
                        <div className="card-header">
                            <h5 className="card-title">Applied</h5>
                        </div>
                        <div className="card-body">
                            <h1>{data.applied}</h1>
                        </div>
                    </div>
                    <div className="card col-2">
                        <div className="card-header">
                            <h5 className="card-title">Phone Interview</h5>
                        </div>
                        <div className="card-body">
                            <h1>{data.phone}</h1>
                        </div>
                    </div>
                    <div className="card col-2">
                        <div className="card-header">
                            <h5 className="card-title">On-site Interview</h5>
                        </div>
                        <div className="card-body">
                            <h1>{data.onsite}</h1>
                        </div>
                    </div>
                    <div className="card col-2">
                        <div className="card-header">
                            <h5 className="card-title">Job Offers</h5>
                        </div>
                        <div className="card-body">
                            <h1>{data.offers}</h1>
                        </div>
                    </div>
                    

                </div>
            </React.Fragment>
        );
    }
}
