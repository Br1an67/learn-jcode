# 部署到 GitHub Pages / Deploy To GitHub Pages

本项目采用 mdBook + GitHub Actions + GitHub Pages：

```text
markdown source -> temporary mdBook source -> mdbook build -> book/ -> GitHub Pages
```

The source of truth remains `README.md`, `README-en.md`, `docs/`, and `mini/`. `scripts/prepare_mdbook_site.py` creates `.mdbook-src/` only for building the website.

## 本地预览 / Local Preview

先安装 `mdbook`，再运行：

```bash
python3 scripts/prepare_mdbook_site.py
mdbook serve --open
```

只构建、不启动服务：

```bash
python3 scripts/prepare_mdbook_site.py
mdbook build
```

构建结果写到 `book/`。`.mdbook-src/` 和 `book/` 都被 `.gitignore` 忽略。

## 发布流程 / GitHub Pages

先在 GitHub 创建你自己的仓库，然后 push：

```bash
git remote add origin git@github.com:<owner>/<repo>.git
git push -u origin main
```

在 GitHub 仓库里设置：

1. 打开 `Settings -> Pages`。
2. 把 `Build and deployment -> Source` 设为 `GitHub Actions`。
3. push 到 `main`，或者在 Actions 页面手动运行 `Deploy mdBook to GitHub Pages`。

`.github/workflows/deploy-pages.yml` 会安装 mdBook、生成 `.mdbook-src/`、构建 `book/`、上传 Pages artifact，然后部署。

## URL 规则 / URL Rule

普通项目仓库的 Pages 地址是：

```text
https://<owner>.github.io/<repo>/
```

如果想占用根地址：

```text
https://<owner>.github.io/
```

仓库名必须是：

```text
<owner>.github.io
```

如果使用自定义域名，在 `Settings -> Pages -> Custom domain` 配。只有确定具体域名后，才需要加 `CNAME` 文件。

## 仓库链接 / Repository Link

`book.toml` 现在没有写 `git-repository-url`，因为最终 GitHub 仓库地址还没确定。确定后可以加：

```toml
[output.html]
git-repository-url = "https://github.com/<owner>/<repo>"
```

不要填 JCode 源码仓库地址。这个链接应该指向教程仓库本身。

## Mermaid

Markdown 里的 Mermaid 代码块由 `mermaid-init.js` 渲染。它会在浏览器加载页面时从 jsDelivr 拉取 Mermaid，所以图表渲染需要浏览器能访问该 CDN。

如果后面要做完全自包含站点，可以把 `mermaid.min.js` vendor 到仓库里，再加入 `book.toml` 的 `additional-js`。
