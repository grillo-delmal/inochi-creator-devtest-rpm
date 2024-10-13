%define inochi_creator_ver 0.8.6
%define inochi_creator_dist 26
%define inochi_creator_short 7d94731

%define inochi_creator_suffix ^%{inochi_creator_dist}.git%{inochi_creator_short}

Name:           inochi-creator-devtest
Version:        %{inochi_creator_ver}%{?inochi_creator_suffix:}
Release:        %autorelease
Summary:        Tool to create and edit Inochi2D puppets

# Bundled lib licenses
##   bcaa licenses: BSL-1.0
##   bindbc-loader licenses: BSL-1.0
##   bindbc-sdl licenses: BSL-1.0
##   dcv licenses: BSL-1.0
##   ddbus licenses: MIT
##   dportals licenses: BSD-2-Clause
##   dunit licenses: MIT
##   dxml licenses: BSL-1.0
##   facetrack-d licenses: BSD-2-Clause
##   fghj licenses: BSL-1.0
##   i18n-d licenses: BSD-2-Clause
##   i2d-imgui licenses: BSL-1.0 and MIT
##   i2d-opengl licenses: BSL-1.0
##   imagefmt licenses: BSD-2-Clause
##   inmath licenses: BSD-2-Clause
##   inochi2d licenses: BSD-2-Clause
##   kra-d licenses: BSD-2-Clause
##   mir-algorithm licenses: Apache-2.0
##   mir-core licenses: Apache-2.0
##   mir-linux-kernel licenses: BSL-1.0
##   mir-random licenses: Apache-2.0
##   psd-d licenses: BSD-2-Clause
##   silly licenses: ISC
##   tinyfiledialogs licenses: Zlib
##   vmc-d licenses: BSD-2-Clause
License:        BSD-2-Clause and Apache-2.0 and BSL-1.0 and ISC and MIT and Zlib

URL:            https://github.com/grillo-delmal/inochi-creator-devtest

Source0:        https://github.com/grillo-delmal/inochi-creator-devtest/releases/download/nightly/inochi-creator-source.zip
Source1:        inochi-creator-devtest.desktop
Source2:        inochi-creator-devtest.appdata.xml
Source3:        dub.selections.json
Source4:        icon.png

# dlang
BuildRequires:  ldc
BuildRequires:  dub
BuildRequires:  jq
BuildRequires:  ldc-libs

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  git

#dportals reqs
BuildRequires:       dbus-devel

#i2d-imgui reqs
BuildRequires:       cmake
BuildRequires:       gcc
BuildRequires:       gcc-c++
BuildRequires:       freetype-devel
BuildRequires:       SDL2-devel

Requires:       hicolor-icon-theme

#dportals deps
Requires:       dbus

#i2d-imgui deps
Requires:       libstdc++
Requires:       freetype
Requires:       SDL2


%description
This is a development test version of the software maintained by Grillo del Mal, use at your own risk.
Inochi2D is a framework for realtime 2D puppet animation which can be used for VTubing, game development and digital animation.
Inochi Creator is a tool that lets you create and edit Inochi2D puppets.

%prep
%setup -c

jq "map(.path = ([\"$(pwd)\"] + (.path | split(\"/\"))[-4:] | join(\"/\")) )" <<<$(<.dub/packages/local-packages.json) > .dub/packages/local-packages.linux.json
rm .dub/packages/local-packages.json
mv .dub/packages/local-packages.linux.json .dub/packages/local-packages.json
dub add-local .flatpak-dub/semver/*/semver
dub add-local .flatpak-dub/gitver/*/gitver

%build
export DFLAGS="%{_d_optflags}"

# Build metadata
dub build --skip-registry=all --compiler=ldc2 --config=update-version
dub build --skip-registry=all --compiler=ldc2 --config=meta

# Build the project, with its main file included, without unittests
dub build --skip-registry=all --compiler=ldc2 --config=barebones --build=debug


%install
install -d ${RPM_BUILD_ROOT}%{_bindir}
install -p ./out/inochi-creator ${RPM_BUILD_ROOT}%{_bindir}/inochi-creator-devtest

install -d ${RPM_BUILD_ROOT}%{_datadir}/applications/
install -p -m 644 %SOURCE1 ${RPM_BUILD_ROOT}%{_datadir}/applications/inochi-creator-devtest.desktop
desktop-file-validate \
    ${RPM_BUILD_ROOT}%{_datadir}/applications/inochi-creator-devtest.desktop

install -d ${RPM_BUILD_ROOT}%{_metainfodir}/
install -p -m 644 %SOURCE2 ${RPM_BUILD_ROOT}%{_metainfodir}/inochi-creator-devtest.appdata.xml
appstream-util validate-relax --nonet \
    ${RPM_BUILD_ROOT}%{_metainfodir}/inochi-creator-devtest.appdata.xml

install -d $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/
install -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/inochi-creator-devtest.png

install -d ${RPM_BUILD_ROOT}%{_datadir}/inochi-creator-devtest/
install -p -m 644 %SOURCE3 ${RPM_BUILD_ROOT}%{_datadir}/inochi-creator-devtest/dub.selections.json


%files
%license LICENSE
%{_bindir}/inochi-creator-devtest
%{_metainfodir}/inochi-creator-devtest.appdata.xml
%{_datadir}/applications/inochi-creator-devtest.desktop
%{_datadir}/icons/hicolor/256x256/apps/inochi-creator-devtest.png
%{_datadir}/inochi-creator-devtest/dub.selections.json


%changelog
%autochangelog
