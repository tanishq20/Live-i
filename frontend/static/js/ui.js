class UI {
  constructor() {
    this.profile = document.getElementById('profile')
  }

  // Display profile in UI
  showProfile(user) {
    this.profile.innerHTML = `
      <div class="card card-body mb-3">
      <div class="row">
        <div class="col-md-3">
          <img class="img-fluid mb-2 rounded-circle shadow-lg" src="${
            user.avatar_url
          }">
          <a href="${
            user.html_url
          }" target="_blank" class="btn btn-primary btn-block">View Profile</a>
        </div>
        <div class="col-md-9">
          <span class="badge bg-primary">Public Repos: ${
            user.public_repos
          }</span>
          <span class="badge bg-secondary">Public Gists: ${
            user.public_gists
          }</span>
          <span class="badge bg-success">Followers: ${user.followers}</span>
          <span class="badge bg-info">Following: ${user.following}</span>
          <br><br>
          <ul class="list-group">
            <li class="list-group-item">Company: ${user.company}</li>
            <li class="list-group-item">Website/Blog: <a href="${
              user.blog
            }" target="_blank" style="text-decoration: none">${
      user.blog
    }</a></li>
            <li class="list-group-item">Location: ${user.location}</li>
            <li class="list-group-item">Member Since: ${user.created_at.slice(
              0,
              user.created_at.indexOf('T')
            )}</li>
          </ul>
        </div>
      </div>
    </div>
    <h3 class="page-heading mb-3">Latest Repos</h3>
    <div id="repos"></div>
      `
  }

  // Show user repos
  showRepos(repos) {
    let output = ''

    repos.forEach((repo) => {
      output += `
          <div class="card card-body mb-2">
            <div class="row">
                <div class="col-md-6">
                    <a href="${repo.html_url}" target="_blank" style="text-decoration: none">${repo.name}</a>
                </div>
                <div class="col-md-6">
                    <span class="badge bg-primary">Stars: ${repo.stargazers_count}</span>
                    <span class="badge bg-secondary">Watchers: ${repo.watchers}</span>
                    <span class="badge bg-success">Forks: ${repo.forks}</span>
                </div>
            </div>
          </div>
          `
    })

    // Output repos
    document.getElementById('repos').innerHTML = output
  }

  // Show alert message
  showAlert(message, className) {
    // Clear any remaining alerts
    this.clearAlert()
    // Create div
    const div = document.createElement('div')
    // Add classes
    div.className = className
    // Add text
    div.appendChild(document.createTextNode(message))
    // Get parent
    const container = document.querySelector('.searchContainer')
    // Get search box
    const search = document.querySelector('.search')
    // Insert alert
    container.insertBefore(div, search)

    // Timeout after 3 sec
    setTimeout(() => {
      this.clearAlert()
    }, 3000)
  }

  // Clear alert message
  clearAlert() {
    const currentAlert = document.querySelector('.alert')

    if (currentAlert) {
      currentAlert.remove()
    }
  }

  // Clear profile
  clearProfile() {
    this.profile.innerHTML = ''
  }
}
