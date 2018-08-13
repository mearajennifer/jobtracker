"use strict";

// Javascript to render profile page info, profile editing

// Parent container -- Profile
class UserProfile extends React.Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleUserSubmit = this.handleUserSubmit.bind(this);
        this.handleUserChange = this.handleUserChange.bind(this);
        this.state = {
            formVisible: false,
            data: null,
            fname: this.props.fname,
            lname: this.props.lname,
            email: this.props.email,
            phone: this.props.phone,
        };
    }

    handleClick(e) {
        e.preventDefault();
        const changeFormVisible = this.state.formVisible == false ? true : false;
        this.setState({
            formVisible: changeFormVisible
        });
    }

    handleUserSubmit(data) {
        this.setState.data = data;

        $.ajax({
            url: '/dashboard/profile/edit',
            type: 'POST',
            data: data,
            success: function (results) {
                this.setState({
                    fname: results.fname,
                    lname: results.lname,
                    email: results.email,
                    phone: results.phone,
                });
            }.bind(this),
            error: function () {
                alert('Error: Please try again.');
            }
        });

        this.setState({formVisible: false});
    }

    handleUserChange(input) {
        this.setState(input);
    }

    render() {
        if (this.state.formVisible === false) {
            return (
                <React.Fragment>
                    <UserGreeting />
                    <UserInformation handleClick={this.handleClick} fname={this.state.fname} lname={this.state.lname} email={this.state.email} phone={this.state.phone} />
                    <UserAnalytics />
                </React.Fragment>
            );
        } else if (this.state.formVisible === true) {
            return (
                <React.Fragment>
                    <UserInformationForm handleClick={this.handleClick} onUserChange={this.handleUserChange} onUserSubmit={this.handleUserSubmit} fname={this.state.fname} lname={this.state.lname} email={this.state.email} phone={this.state.phone} />
                </React.Fragment>
            );
        }
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

// User info component
class UserInformation extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <React.Fragment>
                <div className="row name">
                    <h5>{this.props.fname} {this.props.lname}</h5>
                </div>
                <div className="row">
                    <p>Email: {this.props.email}</p>
                </div>
                <div className="row ">
                    <p>Phone number: {this.props.phone}</p>
                </div>
                <div className="row">
                    <button onClick={this.props.handleClick} type="button" className="btn btn-secondary btn-sm">
                      edit
                    </button>
                </div>
            </React.Fragment>
        );
    }
}

// User info editable form component
class UserInformationForm extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange = (e, inputName) => {
        const input = {};
        input[inputName] = e.target[inputName];

        this.props.onUserChange(input);
    }

    handleSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const data = {};
        let element;
        for (element of form.elements) {
            data[element.name] = element.value;
        }
        this.props.onUserSubmit(data);
    }

    render() {
        return (
            <React.Fragment>
                <form onSubmit={this.handleSubmit}>
                    <div className='form-group'>
                        <label>First name:</label>
                        <input
                          type='text'
                          id='fname-field'
                          className='form-control'
                          value={this.props.fname}
                          onChange={(e) => this.handleChange(e, 'fname')}
                          name='fname'
                          required
                        />
                    </div>

                    <div className='form-group'>
                        <label> Last name:</label>
                        <input
                          type='text'
                          id='lname-field'
                          className='form-control'
                          name='lname'
                          value={this.props.lname}
                          onChange={(e) => this.handleChange(e, 'lname')}
                          required
                        />
                    </div>

                    <div className='form-group'>
                        <label>Email:</label>
                        <input
                          type='email'
                          id='email-field'
                          className='form-control'
                          name='email'
                          value={this.props.email}
                          onChange={(e) => this.handleChange(e, 'email')}
                          required
                        />
                    </div>

                    <div className='form-group'>
                        <label>Phone:</label>
                        <input
                          type='tel'
                          id='tel-field'
                          className='form-control'
                          name='phone'
                          value={this.props.phone}
                          onChange={(e) => this.handleChange(e, 'phone')}
                          pattern='[0-9]{3}-[0-9]{3}-[0-9]{4}'
                        />
                    </div>

                    <div className='form-group'>
                        <button type='button submit' className='btn btn-secondary btn-sm'>
                          submit
                        </button>
                        <a href="" onClick={this.props.handleClick}>cancel</a>
                    </div>

                </form>
            </React.Fragment>
        );
    }
}

// User Analytics component
class UserAnalytics extends React.Component {
    constructor(props) {
        super(props);
    }

    // Need to pass JSON from db/server with stats back to this child element

    render() {
        return (
            <React.Fragment>
                <h5>Your latest job tracking stats:</h5>
                
                <div className="row justify-content-center">

                    <div className="col-fixed ml-auto mr-auto">
                        <div className="card" id="interested">
                            <div className="card-header dark-bg">
                                <h5 className="card-title"><br/>Interested</h5>
                            </div>
                            <div className="card-body justify-content-center">
                                <h1>{data.interested}</h1>
                            </div>
                        </div>
                    </div>
                    <div className="col-fixed ml-auto mr-auto">
                        <div className="card" id="applied">
                            <div className="card-header">
                                <h5 className="card-title"><br/>Applied</h5>
                            </div>
                            <div className="card-body">
                                <h1>{data.applied}</h1>
                            </div>
                        </div>
                    </div>
                    <div className="col-fixed ml-auto mr-auto">
                        <div className="card" id="phone">
                            <div className="card-header">
                                <h5 className="card-title">Phone<br/>Interview</h5>
                            </div>
                            <div className="card-body">
                                <h1>{data.phone}</h1>
                            </div>
                        </div>
                    </div>
                    <div className="col-fixed ml-auto mr-auto">
                        <div className="card" id="onsite">
                            <div className="card-header">
                                <h5 className="card-title">On-site<br/>Interview</h5>
                            </div>
                            <div className="card-body">
                                <h1>{data.onsite}</h1>
                            </div>
                        </div>
                    </div>
                    <div className="col-fixed ml-auto mr-auto">
                        <div className="card" id="offers">
                            <div className="card-header">
                                <h5 className="card-title"><br/>Job Offers</h5>
                            </div>
                            <div className="card-body">
                                <h1>{data.offers}</h1>
                            </div>
                        </div>
                    </div>                    

                </div>
            </React.Fragment>
        );
    }
}
