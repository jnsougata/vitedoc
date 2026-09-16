import { defineConfig } from "vitepress";

export default defineConfig({
    base: "/vitedoc/",
    title: "vitedoc",
    description: "An automatic documentation generator for vitepress.",
    cleanUrls: true,

    head: [
    [
        "link",
        {
            "rel": "icon",
            "href": "/logo.png"
        }
    ]
],

    themeConfig: {
        logo: "/logo.png",

        nav: [],

        editLink: {
            pattern: "",
        },

        sidebar: [
    {
        "text": "Introduction",
        "link": "/guide/0.1.dev0/introduction"
    },
    {
        "text": "Reference",
        "items": [
            {
                "text": "Autodoc",
                "link": "/guide/0.1.dev0/autodoc"
            },
            {
                "text": "Client",
                "link": "/guide/0.1.dev0/client"
            },
            {
                "text": "Config",
                "link": "/guide/0.1.dev0/config"
            },
            {
                "text": "Home",
                "link": "/guide/0.1.dev0/home"
            },
            {
                "text": "Mapper",
                "link": "/guide/0.1.dev0/mapper"
            },
            {
                "text": "Package",
                "link": "/guide/0.1.dev0/package"
            },
            {
                "text": "Sidebar",
                "link": "/guide/0.1.dev0/sidebar"
            },
            {
                "text": "Utils",
                "link": "/guide/0.1.dev0/utils"
            }
        ]
    }
],

        search: {
            provider: "local",
            options: {
                _render: (src, env, md) => {
                    if (env.relativePath.startsWith("docs")) {
                        return "";
                    }
                    return md.render(src, env);
                },
            },
        },

        socialLinks: [],
    },
});
