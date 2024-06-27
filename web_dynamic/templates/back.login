<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title></title>
	<link rel="stylesheet" href="../static/styles/auth_form.css?{{ cache_id }}" media="all">
	<link rel="stylesheet" href="../static/styles/header.css?{{ cache_id }}" media="all">
	<script src="https://code.jquery.com/jquery-3.2.1.min.js"></script>
	<script src="../static/scripts/auth.js?{{ cache_id }}"></script>

</head>
<body>
	<header class="header">SpendSmart</header>
	{% with messages = get_flashed_messages() %}
	{% if messages %}
		{% for message in messages %}
		<div class="toast">{{ message }}</div>
		{% endfor %}
	{% endif %}
	{% endwith %}
	<form method="POST" action="/login"class="auth-form">
		<h1>Login</h1>
		<div class="email-container">
		<h3>Enter email or username</h3>
		<input class="email-input" type="text" name="email_or_name" required="required">
		</div>
		<div class="password-container">
		<h3>Enter Password</h3>
		<input class="password-input" type="password" name="password" required="required">
		</div>
		<div class="goto-container">
			<div class="remember">
				<input class="checkbox" type="checkbox" name="remember">
				<label for="remember">Remember me</label>
			</div>
			<a class="signup" href="{{ url_for('auth.signup') }}">Signup</a>
		</div>
		<div class="submit-container">
			<input type="submit" class="submit" value="Login">
		</div>
	</form>


</body>
</html>
