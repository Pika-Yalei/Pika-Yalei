# Public badge references

The README follows [t8y2’s profile](https://github.com/t8y2/t8y2/blob/main/README.md): Shields `flat-square` badges with community-maintained Simple Icons. These are external public images, not first-party brand artwork or locally drawn images.

[Shields logo documentation](https://shields.io/docs/logos) · [Simple Icons current slugs](https://github.com/simple-icons/simple-icons/blob/develop/slugs.md)

The 32 technologies are a concise selection of tools used in development, not a claim of expert proficiency. Their absence does not imply unfamiliarity.

Existing matching URLs are preserved. Spring Boot, Vite, Tailwind CSS and RocksDB use documented `springboot`, `vite`, `tailwindcss` and `rocksdb` slugs. Flink CDC uses the Apache Flink icon (`apacheflink`), not an invented separate CDC logo. Compose uses Docker, Shell uses GNU Bash, and Java uses OpenJDK.

Oracle, SQL Server, 达梦 and VS Code use Shields' documented `logo=data:image/svg+xml;base64,...` option. Oracle and VS Code retain the original SVG bytes. SQL Server and 达梦 use 32×32 transparent PNG adaptations of the same existing SVG paths: monochrome white on a red badge background. Only color and raster resolution change; the path geometry is not redrawn.

This environment previously received HTTP 403 from the image service. No proxy or alternate exit is used. URL syntax and catalogue slugs are validated; successful image loading is not claimed.

## Custom logo provenance

Oracle, SQL Server and 达梦 are community-collected assets from DBX, not claimed to be first-party authorized artwork. VS Code is the original SVG extracted from Microsoft's published branding ZIP (`visual-studio-code-icons/vscode.svg`). The logos identify technologies used; no affiliation, certification, sponsorship or endorsement is implied. Copyrights and trademarks remain with their respective owners. A repository software license is not a grant of third-party trademark rights.

- **Oracle**: [source](https://github.com/t8y2/dbx/blob/9e2485531c91c7304ca17b8e77482f72bd192f64/apps/desktop/public/icons/database/oracle.svg), SHA-256 `4ba0e2685ed5d2fdbb08b71948664264aaaa74a9e1155f395ff8a0ed7b2153ef`.
- **SQL Server**: [source](https://github.com/t8y2/dbx/blob/9e2485531c91c7304ca17b8e77482f72bd192f64/apps/desktop/public/icons/database/sqlserver.svg), SHA-256 `7656a497e805c21762d7a67b9e9cd638f101f0bff562254258d682aac406014d`.
- **达梦**: [source](https://github.com/t8y2/dbx/blob/9e2485531c91c7304ca17b8e77482f72bd192f64/apps/desktop/public/icons/database/dm.svg), SHA-256 `54e9b794c86762664b23ac07c12016aecfbc3a309e4ce432b768ed0226862a44`.
- **VS Code**: [source](https://code.visualstudio.com/assets/branding/visual-studio-code-icons.zip), SHA-256 `74ad401c6487a0dc5af1f6b2935556ab2d3553ae45effc7e1697b4d117d046b6`.

[Shields Custom Logos](https://shields.io/docs/logos#custom-logos) · [DBX license](https://github.com/t8y2/dbx/blob/9e2485531c91c7304ca17b8e77482f72bd192f64/LICENSE) · [VS Code brand guidance](https://code.visualstudio.com/brand)

The SVG data URIs match their original source bytes; the PNG data URIs match the documented derivative files. The image service was not requested again after the earlier HTTP 403; rendered badge loading has not been asserted.

## SQL Server / 达梦 rendering repair

The previous SQL Server URL was 6,934 bytes and its GitHub-rendered Camo URL was 13,968 bytes. The HTML contained the full URL. Its loading failure was reported by the user; URL/header length is a suspected contributor, not a proven server response diagnosis.

Both symbols retain the DBX source geometry above. All original path `d` attributes were checked unchanged before rasterization. Color is adapted to white for legibility. Inkscape renders the source at 32×32; PNG compression preserves those raster pixels. This is a derived display asset, not an unmodified original SVG.

- SQL Server: 32×32 PNG, 863 bytes, SHA-256 `38d87bbffc74e364a4e230ed9771e8ade37ed2bb42fab9119dad2373c09eb98d`.
- 达梦: 32×32 PNG, 489 bytes, SHA-256 `708e9fe8c3e8481bd53851b9e3f6a301dfb138443b50b5a5c7e120c9de354da5`.

[Shields official data-URI handling](https://github.com/badges/shields/blob/master/lib/logos.js) accepts PNG. The official `badge-maker` 6.0.0 renderer was used locally to compare 28/32px inputs at normal badge size and inspect the final pixels. These preview outputs are not committed or substituted for the public image service. They verify local rendering only, not delivery from Shields/GitHub Camo; neither service was requested to bypass the earlier denial.
