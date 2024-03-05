'use strict'

let prevSelectedId = undefined;

function getPos(element) {
    return element.getBoundingClientRect().top - document.body.getBoundingClientRect().top;
}

let screenOffset = NaN;

function makeScreenOffset() {
    const val = window.innerHeight / 2;
    console.log(val);
    return val;
}

let headings = undefined;

function makeHeadings() {
    const content_region = document.getElementsByTagName("devsite-content")[0];
    if (content_region === undefined) return;
    const headings = ["h2", "h3", "h4", "h5", "h6"]
        .map(x => Array.from(content_region.getElementsByTagName(x)))
        .flat() 
        .map(el => {
            const id = el.id;
            if (id === undefined) return null;
            return {
                id,
                posY: getPos(el),
            };
        })
        // do we need this?
        .filter(x => x !== null)
        .sort((a, b) => {
            return a.posY > b.posY;
        });
    return headings;
}

let tocEntries = undefined;

function makeTocEntries() {
    const devsiteToc = document.getElementsByTagName("devsite-toc")[0];
    if (devsiteToc === undefined) return;
    const entries = Array.from(devsiteToc.getElementsByTagName("li"))
        .map(el => {
            const anchor_child = el.children[0];
            if (anchor_child === undefined) return null;
            if (anchor_child.tagName !== "A") return null;
            const id = anchor_child.href.replaceAll(/^.*\#/g, ""); 
            return {
                id,
                anchorElement: anchor_child,
            };
        })
        .filter(x => x !== null);
    return entries;
}

function onScroll() {
    if (isNaN(screenOffset)) {
        screenOffset = makeScreenOffset();
    }

    if (headings === undefined) {
        headings = makeHeadings();
    }
    
    if (tocEntries === undefined) {
        tocEntries = makeTocEntries();
    }
        
    let elementSelectedIdx = headings.length - 1;
    headings.some(({ id, posY: elementY }, i) => {
        const { scrollY } = window;
        if (elementY - screenOffset > scrollY) {
            elementSelectedIdx = i - 1;
            return true;
        }
    });
    const elementSelectedId = headings[Math.max(elementSelectedIdx, 0)]?.id;
    if (elementSelectedId === prevSelectedId) return;
    prevSelectedId = elementSelectedId;
    tocEntries.forEach(({ id, anchorElement }) => {
        if (id === elementSelectedId) {
            anchorElement.classList.add("devsite-nav-active");
        } else {
            anchorElement.classList.remove("devsite-nav-active");
        }
    });
    console.log("Select:", elementSelectedId);
}

function onResize() {
    screenOffset = makeScreenOffset();
    headings = makeHeadings();
}

window.addEventListener("scroll", onScroll);
window.addEventListener("resize", onResize);
