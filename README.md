<p align="center">
  <img src="packaging/icon/monogram.png" alt="SP" width="160"><br>
  <img src="docs/images/spartanport-logo.png" alt="SpartanPort" width="600">
</p>

# SpartanPort for macOS

**SpartanPort for macOS** is an unofficial build of [SpartanPort](https://github.com/FelipePrado0/SpartanPort),
the unofficial port of **God of War III Remastered** (PlayStation 4), for Macs with Apple Silicon.

This fork is where the Apple Silicon work started. It has been contributed to the original
project in [FelipePrado0/SpartanPort#798](https://github.com/FelipePrado0/SpartanPort/pull/798),
which now publishes an official macOS test package. **To play, use that package** (below).
For Windows and Linux, use the [original project](https://github.com/FelipePrado0/SpartanPort).

> **No game files are included.** You need a dump from your own PS4 (tested: CUSA01623 and
> CUSA01715, versions 01.00 and 01.02).
> This project is not affiliated with or endorsed by Sony Interactive Entertainment or Santa Monica Studio.
> God of War is a trademark of Sony Interactive Entertainment.

## Contents

- [Requirements](#requirements)
- [Download and play](#download-and-play)
- [Performance](#performance)
- [Settings](#settings)
- [Keyboard controls](#keyboard-controls)
- [Troubleshooting](#troubleshooting)
- [Building from source](#building-from-source)
- [How it works on a Mac](#how-it-works-on-a-mac)
- [Credits](#credits)
- [License](#license)

## Requirements

- A Mac with **Apple Silicon** (M1 or newer). Intel Macs are not supported.
- **macOS 26 (Tahoe) or newer.** The Vulkan driver this build uses (Mesa's KosmicKrisp) needs
  it; macOS 14 Sonoma and 15 Sequoia cannot run it.
- **Rosetta 2** (macOS offers to install it the first time).
- Your own dump of the game (the folder with `eboot.bin`, `sce_module` and `sce_sys`).

## Download and play

1. Download `spartanport-macos.dmg` from the original project's
   [macOS test release](https://github.com/FelipePrado0/SpartanPort/releases/tag/macos-v2.6.0-apple-silicon-test1)
   (check its `.sha256` file if you want to verify the download).
2. Open the DMG and drag **SpartanPort.app** into **Applications**.
3. Open SpartanPort and choose your game folder in the launcher.

The test app has an ad hoc signature, not Apple notarization. If macOS refuses to open it,
first make sure it came from the release page above, then remove the download flag:

```bash
xattr -dr com.apple.quarantine /Applications/SpartanPort.app
```

Do not turn off Gatekeeper globally. Saves, settings, logs and caches are kept in
`~/Library/Application Support/SpartanPort`, outside the app, so replacing the app keeps them.

Start at **720p** with a 60 FPS engine rate and frame limit. When you report results in
[#798](https://github.com/FelipePrado0/SpartanPort/pull/798), include your Mac model, RAM,
macOS version, game version, resolution, the scene and the launcher's exported log.

## Performance

Measured on an M1 Max (32-core GPU), scripted two-minute fights in the first Gaia level:

| Render resolution | Average FPS | Most of the time |
|---|---|---|
| 720p (recommended) | 58-60 | 52-60 |
| Native 1080p | 41 | 37-46 |

The game is limited by the GPU there (98-99% busy). Smaller Apple Silicon chips have fewer GPU
cores and will be slower; 720p is the setting to start with.

## Settings

The launcher's settings and the in-game menu (**Insert**, the key left of **1**, or **R3 + L2**
on a controller) change the render resolution, the engine frame rate and the frame limit. A
source build keeps them in `spartanport.ini` in its folder. Live render-scale changes are off on
this driver; the startup resolution still applies. The game's multisampling is off by default on
macOS (the driver reads the 2-sample depth buffer wrong: an unlit, fully fogged scene).

## Keyboard controls

Defaults; change them on the launcher's **Controls** page. Controllers (DualSense, Xbox and
others) work as well.

| Key | Button |
|---|---|
| WASD | left stick |
| Arrows | right stick (camera) |
| Space | Cross |
| Left Shift | Circle |
| Left click | Square |
| Right click | Triangle |
| Q and E | L1 and R1 |
| R and the mouse's forward button | L2 and R2 |
| Z and X | L3 and R3 |
| Wheel click | Rage of Sparta (L3 + R3) |
| C | Grab (L1 + Circle) |
| The mouse's back button | Dodge |
| 1, 2, 3, 4 | d-pad up, right, down, left (weapons) |
| Tab | Options |
| P | left touchpad click (photo mode) |
| Esc | right touchpad click (pause menu) |
| Insert | the port's menu (R3+L2 on the controller) |

Without the launcher the game keeps its own keys: E and Q for Square and Triangle, 1 and 3 for
L1 and R1, F for R2, C for R3, I, K, J, L for the d-pad, Enter for Options, Tab and Backspace for
the touchpad.

## Troubleshooting

- **"SpartanPort can't be opened" or "is damaged":** the download flag; see
  [Download and play](#download-and-play).
- **"Would like to access files in your Desktop/Documents folder":** click **Allow** if your game
  dump is there.
- **Low frame rate:** use 720p, and close other apps that use the GPU (video players, browsers
  with many tabs).
- **Your Mac runs macOS 14 or 15:** not supported (see [Requirements](#requirements)).
- **A source build stops with "Need the x86-64 dependencies":** run
  `bash packaging/macos/build-deps.sh` (again).
- **Anything else:** report it in [#798](https://github.com/FelipePrado0/SpartanPort/pull/798)
  with the launcher's exported log.

## Building from source

For developers. Needs Xcode or its Command Line Tools and [Homebrew](https://brew.sh). The first
build takes a while: it compiles the x86-64 libraries (SDL3, FFmpeg, Vulkan loader, KosmicKrisp)
into `~/Library/Caches/spartanport-macos-deps`.

```bash
git clone --recursive https://github.com/Fleurat/SpartanPort-macOS
cd SpartanPort-macOS
bash packaging/macos/build-deps.sh
bash build.sh
SPARTAN_GAME_DIR=/path/to/CUSA01623 bash run.sh
```

The launcher needs Tk for Homebrew's Python; its PLAY button starts the game without rebuilding:

```bash
brew install python-tk
python3 launcher/spartanport_launcher_win.py
```

Without the launcher, `bash packaging/macos/make-app.sh` puts a `SpartanPort.app` on the
desktop that asks for the render resolution and starts the game without Terminal. Both run the
checkout as built: run `bash build.sh` again after pulling changes. `bash build.sh --test` runs
the C tests.

## How it works on a Mac

- **CPU:** the game's original x86-64 code runs under Rosetta 2, with the same runtime as on
  Linux. macOS reserves the address range the PS4 uses, so the game's memory starts at
  `0x7000000000`; the game's thread data is a pthread key, which Rosetta exposes through `gs`.
- **Graphics:** shadPS4's video core translates the PS4 GPU commands and shaders to Vulkan, and
  Mesa's KosmicKrisp driver runs Vulkan on Metal. MoltenVK lacks features the renderer needs.
- **Speed work for Apple GPUs** (`packaging/macos/kosmickrisp-spartanport.patch`, the renderer):
  PS4 rect lists are drawn through tessellation, which KosmicKrisp runs as a compute pre-pass that
  interrupts the Metal render pass. Most of the game's rect lists need no draw at all (empty
  draws and depth clears the render pass already does), so they are skipped or folded into the
  next pass. The driver is also built so that Rosetta does not run its hot copies through a slow
  instruction (`rep movsb`).

## Credits

- **[Felipe Prado](https://github.com/FelipePrado0)** and the
  [SpartanPort](https://github.com/FelipePrado0/SpartanPort) contributors: the port itself and
  its official macOS package, which combines this work with
  [nizwar's #510](https://github.com/FelipePrado0/SpartanPort/pull/510) (app packaging) and
  [Incognito-Coder's #469](https://github.com/FelipePrado0/SpartanPort/pull/469) (build
  automation, CoreAudio).
- **deadinside28** ([bloodborne_pc](https://github.com/deadinside28/bloodborne_pc)) and
  **Supermedo** ([bloodborne_pc for Windows](https://github.com/Supermedo/bloodborne_pc)): the
  native port SpartanPort comes from.
- **cuesta4** ([shadPS4 `eltutz`](https://github.com/cuesta4/shadPS4/tree/eltutz)) and the
  **[shadPS4](https://github.com/shadps4-emu/shadPS4)** team: the video core and this game's
  rendering fixes.
- **Mesa's [KosmicKrisp](https://gitlab.freedesktop.org/mesa/mesa)** developers: Vulkan on Metal.
- Patches by kvicken and cuesta4 (building on illusion0001's PS3 patches); cheats adapted from
  Celogamez's GoldHEN cheats. Full list in the
  [original README](https://github.com/FelipePrado0/SpartanPort#credits).

## License

GNU GPL v2 or later ([LICENSE](LICENSE)). Third-party components keep their own licenses.
