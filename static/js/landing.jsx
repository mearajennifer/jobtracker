'use strict';

// React components to render landing page

// Parent container
class Landing extends React.Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.handleUserSubmit = this.handleUserSubmit.bind(this);
        this.state = { 
            formType: 'login',
            data: null,
        };
    }

    handleClick(e) {
        e.preventDefault();
        const newForm = this.state.formType == 'login' ? 'registration' : 'login';
        this.setState({
            formType: newForm
        });
    }

    handleUserSubmit(data) {
        this.setState.data = data;

        $.ajax({
            url: '/register',
            type: 'POST',
            // dataType: 'json',
            data: data,
            success: function (resp) {
                alert(resp);
            },
            error: function () {
                alert('Error: Please try again.');
            }
        });
        
        this.setState({formType: 'login'});        
    }

    render() {
        if (this.state.formType === 'login') {
            return (<Login handleClick={this.handleClick} />);
        } else if (this.state.formType === 'registration') {
            return (<Registration handleClick={this.handleClick} onUserSubmit={this.handleUserSubmit} />);
        }
    }

}

// Login container (default)
class Login extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const marginStyle = {
            marginTop: '15%'
        };

        return (
            <div className='jumbotron' style={marginStyle}>
                <img src='/static/img/JobTracker-nobg2.png' width='100%' className="text-center" />
                <hr className='my-4' />
                <div id='login-form'>
                    <form action='/login' method='POST'>
                        <div className='form-group'>
                            <label>Email: </label>
                            <input type='email' className='form-control' name='email' />
                        </div>

                        <div className='form-group'>
                            <label>Password:</label>
                            <input type='password' className='form-control' name='password' />
                        </div>

                        <div className='form-group'>
                            <button type='button submit' className='btn btn-secondary btn-sm'>Sign In</button>
                        </div>
                    </form>
                    <hr className='my-4' />
                    New to JobTracker? <a href='' onClick={this.props.handleClick}>Register</a>
                </div>
            </div>
        );
    }
}


// Registration container
class Registration extends React.Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
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
        const marginStyle = {
            marginTop: '5px'
        };

        return (
            <div className='jumbotron' style={marginStyle}>
                <img src='/static/img/JobTracker-nobg2.png' width='100%' className="text-center" />
                <hr className='my-4' />
                <div id='registration-form'>
                    <form onSubmit={this.handleSubmit}>

                        <div className='form-group'>
                            <label>First name:</label>
                            <input type='text' id='fname-field' className='form-control' name='fname' placeholder='Jane' required />
                        </div>

                        <div className='form-group'>
                            <label> Last name:</label>
                            <input type='text' id='lname-field' className='form-control' name='lname' placeholder='Jobseeker' required />
                        </div>

                        <div className='form-group'>
                            <label>Email:</label>
                            <input type='email' id='email-field' className='form-control' name='email' placeholder='jane@jobseeker.com' required />
                        </div>

                        <div className='form-group'>
                            <label>Phone number:</label>
                            <input type='tel' id='tel-field' className='form-control' name='phone' placeholder='123-456-7890' pattern='[0-9]{3}-[0-9]{3}-[0-9]{4}' />
                        </div>

                        <div className='form-group'>
                            <label>Password: </label>
                            <input type='password' id='password-field' className='form-control' name='password' required />
                        </div>

                        <div className='form-group'>
                            <button type='button submit' className='btn btn-secondary btn-sm'>Register</button>
                        </div>
                    </form>
                    <hr className='my-4' />
                    Have an account? <a href='' onClick={this.props.handleClick}>Sign In</a>
                </div>
            </div>
        );
    }
}

// render landing component
ReactDOM.render(
  <Landing />,
  document.getElementById('landing')
);
