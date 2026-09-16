---
title: vitedoc.utils
---

# `vitedoc.utils`

## Classes

- [Action](#class-action)
- [Feature](#class-feature)

<a id="class-action"></a>
## Action

`vitedoc.utils.Action`

Represents an action element.
#### _Arguments_

- _**theme** (`str`): The name of the theme. Supported themes are `brand` and `alt`._
- _**text** (`str`): The text to display on the action button._
- _**link** (`str`): The URL to navigate to when the action button is clicked._


<a id="class-feature"></a>
## Feature

`vitedoc.utils.Feature`

Represents a feature element.
#### _Arguments_

- _**icon_emoji** (`str`): The emoji icon to use. Defaults to None._
- _**icon_path** (`str`): The path to the icon. Defaults to None._
- _**title** (`str`): The title of the feature. Defaults to None._
- _**details** (`str`): The details of the feature. Defaults to None._
#### _Notes_

> `icon_emoji` and `icon_path` mutually exclusive. If both are provided, `icon_emoji` will take precedence.

