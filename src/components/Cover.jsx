import { CoverArt } from "./CoverArt";

export function Cover({author, title}) {
    return (
        <div className="cover">
            <CoverArt />
            <div className="cover-title">{title.toLowerCase()}</div>
            <div className="cover-author">{author.toLowerCase()}</div>
        </div>
    )
}