
![build](https://github.com/prius/leetcode-anki/actions/workflows/build-deck.yml/badge.svg)
![style](https://github.com/prius/leetcode-anki/actions/workflows/style-check.yml/badge.svg)
![tests](https://github.com/prius/leetcode-anki/actions/workflows/tests.yml/badge.svg)
![types](https://github.com/prius/leetcode-anki/actions/workflows/type-check.yml/badge.svg)
![license](https://img.shields.io/github/license/prius/leetcode-anki)

# Leetcode Anki card generator

## Summary
By running this script you'll be able to generate Anki cards with ~~all the leetcode problems~~ problems in Obsidian files.

I personally use it to track my grinding progress.

## Prerequisites
1. [python3.8+](https://www.python.org/downloads/) installed
2. [python virtualenv](https://pypi.org/project/virtualenv/) installed
3. [git cli](https://github.com/git-guides/install-git) installed
4. [GNU make](https://www.gnu.org/software/make/) installed (optional, can run the script directly)
5. \*nix operating system (Linux, MacOS, FreeBSD, ...). Should also work for Windows, but commands will be different. I'm not a Windows expert, so can't figure out how to make it work there, but contributions are welcome.

## How to use

1. Use dataviewJs to format notes
```
const folder = "leetcode"
const files = dv.pages(`"${folder}"`)

files.forEach(file => {
	if (file.file.tags.length > 0) {
		const fileName = file.file.name
		const fileLink = file.Link
		dv.paragraph(`${fileLink}, ${fileName}`)
	}
})
```
2. Run script to generate deck
```
pip install -r requirements.txt
python generate.py
```
3. You'll get `leetcode.apkg` file, which you can import directly to your anki app.
