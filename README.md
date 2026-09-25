# Jonathan Hustead — Portfolio

Astro portfolio for [jonathanhustead.com](https://jonathanhustead.com).

## Stack

- Astro 7 (static output)
- TypeScript
- Native CSS (no UI framework)
- Web3Forms for contact
- `@astrojs/sitemap` for SEO

## Develop

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
npm run preview
```

## Contact form

Copy `.env.example` to `.env` and set `PUBLIC_WEB3FORMS_ACCESS_KEY` if you need to override the default access key.

## Content

Site copy, experience, education, skills, and project metadata live in `src/data/site.ts`. Resume PDF and project images are under `public/`.
