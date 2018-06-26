export const imports = {
  'CHANGELOG.mdx': () =>
    import(/* webpackPrefetch: true, webpackChunkName: "changelog" */ 'CHANGELOG.mdx'),
  'FAQ.mdx': () =>
    import(/* webpackPrefetch: true, webpackChunkName: "faq" */ 'FAQ.mdx'),
}
