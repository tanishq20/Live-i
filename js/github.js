class Github {
  constructor() {
    this.client_id = 'a7fe8c344fd58bbd816f'
    this.client_secret = 'c2086f34312821ec244321c50f5d440b5364b6ea'
    this.repos_count = 5
    this.repos_sort = 'created: asc'
  }

  async getUser(user) {
    const profileResponse = await fetch(
      `https://api.github.com/users/${user}?client_id=${this.client_id}&client_secret=${this.client_secret}`
    )
    const repoResponse = await fetch(
      `https://api.github.com/users/${user}/repos?client_id=${this.client_id}&client_secret=${this.client_secret}`
    )

    const profileData = await profileResponse.json()
    const repoData = await repoResponse.json()

    return {
      profile: profileData,
      repo: repoData,
    }
  }
}
