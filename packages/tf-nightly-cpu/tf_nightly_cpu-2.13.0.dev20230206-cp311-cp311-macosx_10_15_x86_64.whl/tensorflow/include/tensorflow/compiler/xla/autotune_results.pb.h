// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tensorflow/compiler/xla/autotune_results.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fxla_2fautotune_5fresults_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fxla_2fautotune_5fresults_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
#include "tensorflow/tsl/protobuf/autotuning.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tensorflow_2fcompiler_2fxla_2fautotune_5fresults_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tensorflow_2fcompiler_2fxla_2fautotune_5fresults_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tensorflow_2fcompiler_2fxla_2fautotune_5fresults_2eproto;
namespace xla {
class AutotuneResults;
struct AutotuneResultsDefaultTypeInternal;
extern AutotuneResultsDefaultTypeInternal _AutotuneResults_default_instance_;
class AutotuneResults_Entry;
struct AutotuneResults_EntryDefaultTypeInternal;
extern AutotuneResults_EntryDefaultTypeInternal _AutotuneResults_Entry_default_instance_;
}  // namespace xla
PROTOBUF_NAMESPACE_OPEN
template<> ::xla::AutotuneResults* Arena::CreateMaybeMessage<::xla::AutotuneResults>(Arena*);
template<> ::xla::AutotuneResults_Entry* Arena::CreateMaybeMessage<::xla::AutotuneResults_Entry>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace xla {

// ===================================================================

class AutotuneResults_Entry final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:xla.AutotuneResults.Entry) */ {
 public:
  inline AutotuneResults_Entry() : AutotuneResults_Entry(nullptr) {}
  ~AutotuneResults_Entry() override;
  explicit PROTOBUF_CONSTEXPR AutotuneResults_Entry(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  AutotuneResults_Entry(const AutotuneResults_Entry& from);
  AutotuneResults_Entry(AutotuneResults_Entry&& from) noexcept
    : AutotuneResults_Entry() {
    *this = ::std::move(from);
  }

  inline AutotuneResults_Entry& operator=(const AutotuneResults_Entry& from) {
    CopyFrom(from);
    return *this;
  }
  inline AutotuneResults_Entry& operator=(AutotuneResults_Entry&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const AutotuneResults_Entry& default_instance() {
    return *internal_default_instance();
  }
  static inline const AutotuneResults_Entry* internal_default_instance() {
    return reinterpret_cast<const AutotuneResults_Entry*>(
               &_AutotuneResults_Entry_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(AutotuneResults_Entry& a, AutotuneResults_Entry& b) {
    a.Swap(&b);
  }
  inline void Swap(AutotuneResults_Entry* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(AutotuneResults_Entry* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  AutotuneResults_Entry* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<AutotuneResults_Entry>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const AutotuneResults_Entry& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const AutotuneResults_Entry& from) {
    AutotuneResults_Entry::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(AutotuneResults_Entry* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "xla.AutotuneResults.Entry";
  }
  protected:
  explicit AutotuneResults_Entry(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kDeviceFieldNumber = 1,
    kHloFieldNumber = 2,
    kResultFieldNumber = 3,
  };
  // string device = 1;
  void clear_device();
  const std::string& device() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_device(ArgT0&& arg0, ArgT... args);
  std::string* mutable_device();
  PROTOBUF_NODISCARD std::string* release_device();
  void set_allocated_device(std::string* device);
  private:
  const std::string& _internal_device() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_device(const std::string& value);
  std::string* _internal_mutable_device();
  public:

  // string hlo = 2;
  void clear_hlo();
  const std::string& hlo() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_hlo(ArgT0&& arg0, ArgT... args);
  std::string* mutable_hlo();
  PROTOBUF_NODISCARD std::string* release_hlo();
  void set_allocated_hlo(std::string* hlo);
  private:
  const std::string& _internal_hlo() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_hlo(const std::string& value);
  std::string* _internal_mutable_hlo();
  public:

  // .tensorflow.AutotuneResult result = 3;
  bool has_result() const;
  private:
  bool _internal_has_result() const;
  public:
  void clear_result();
  const ::tensorflow::AutotuneResult& result() const;
  PROTOBUF_NODISCARD ::tensorflow::AutotuneResult* release_result();
  ::tensorflow::AutotuneResult* mutable_result();
  void set_allocated_result(::tensorflow::AutotuneResult* result);
  private:
  const ::tensorflow::AutotuneResult& _internal_result() const;
  ::tensorflow::AutotuneResult* _internal_mutable_result();
  public:
  void unsafe_arena_set_allocated_result(
      ::tensorflow::AutotuneResult* result);
  ::tensorflow::AutotuneResult* unsafe_arena_release_result();

  // @@protoc_insertion_point(class_scope:xla.AutotuneResults.Entry)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr device_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr hlo_;
    ::tensorflow::AutotuneResult* result_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcompiler_2fxla_2fautotune_5fresults_2eproto;
};
// -------------------------------------------------------------------

class AutotuneResults final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:xla.AutotuneResults) */ {
 public:
  inline AutotuneResults() : AutotuneResults(nullptr) {}
  ~AutotuneResults() override;
  explicit PROTOBUF_CONSTEXPR AutotuneResults(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  AutotuneResults(const AutotuneResults& from);
  AutotuneResults(AutotuneResults&& from) noexcept
    : AutotuneResults() {
    *this = ::std::move(from);
  }

  inline AutotuneResults& operator=(const AutotuneResults& from) {
    CopyFrom(from);
    return *this;
  }
  inline AutotuneResults& operator=(AutotuneResults&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const AutotuneResults& default_instance() {
    return *internal_default_instance();
  }
  static inline const AutotuneResults* internal_default_instance() {
    return reinterpret_cast<const AutotuneResults*>(
               &_AutotuneResults_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(AutotuneResults& a, AutotuneResults& b) {
    a.Swap(&b);
  }
  inline void Swap(AutotuneResults* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(AutotuneResults* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  AutotuneResults* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<AutotuneResults>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const AutotuneResults& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const AutotuneResults& from) {
    AutotuneResults::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(AutotuneResults* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "xla.AutotuneResults";
  }
  protected:
  explicit AutotuneResults(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  typedef AutotuneResults_Entry Entry;

  // accessors -------------------------------------------------------

  enum : int {
    kDotsFieldNumber = 2,
    kConvsFieldNumber = 3,
    kVersionFieldNumber = 1,
  };
  // repeated .xla.AutotuneResults.Entry dots = 2;
  int dots_size() const;
  private:
  int _internal_dots_size() const;
  public:
  void clear_dots();
  ::xla::AutotuneResults_Entry* mutable_dots(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::AutotuneResults_Entry >*
      mutable_dots();
  private:
  const ::xla::AutotuneResults_Entry& _internal_dots(int index) const;
  ::xla::AutotuneResults_Entry* _internal_add_dots();
  public:
  const ::xla::AutotuneResults_Entry& dots(int index) const;
  ::xla::AutotuneResults_Entry* add_dots();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::AutotuneResults_Entry >&
      dots() const;

  // repeated .xla.AutotuneResults.Entry convs = 3;
  int convs_size() const;
  private:
  int _internal_convs_size() const;
  public:
  void clear_convs();
  ::xla::AutotuneResults_Entry* mutable_convs(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::AutotuneResults_Entry >*
      mutable_convs();
  private:
  const ::xla::AutotuneResults_Entry& _internal_convs(int index) const;
  ::xla::AutotuneResults_Entry* _internal_add_convs();
  public:
  const ::xla::AutotuneResults_Entry& convs(int index) const;
  ::xla::AutotuneResults_Entry* add_convs();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::AutotuneResults_Entry >&
      convs() const;

  // int32 version = 1;
  void clear_version();
  int32_t version() const;
  void set_version(int32_t value);
  private:
  int32_t _internal_version() const;
  void _internal_set_version(int32_t value);
  public:

  // @@protoc_insertion_point(class_scope:xla.AutotuneResults)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::AutotuneResults_Entry > dots_;
    ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::AutotuneResults_Entry > convs_;
    int32_t version_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tensorflow_2fcompiler_2fxla_2fautotune_5fresults_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// AutotuneResults_Entry

// string device = 1;
inline void AutotuneResults_Entry::clear_device() {
  _impl_.device_.ClearToEmpty();
}
inline const std::string& AutotuneResults_Entry::device() const {
  // @@protoc_insertion_point(field_get:xla.AutotuneResults.Entry.device)
  return _internal_device();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void AutotuneResults_Entry::set_device(ArgT0&& arg0, ArgT... args) {
 
 _impl_.device_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:xla.AutotuneResults.Entry.device)
}
inline std::string* AutotuneResults_Entry::mutable_device() {
  std::string* _s = _internal_mutable_device();
  // @@protoc_insertion_point(field_mutable:xla.AutotuneResults.Entry.device)
  return _s;
}
inline const std::string& AutotuneResults_Entry::_internal_device() const {
  return _impl_.device_.Get();
}
inline void AutotuneResults_Entry::_internal_set_device(const std::string& value) {
  
  _impl_.device_.Set(value, GetArenaForAllocation());
}
inline std::string* AutotuneResults_Entry::_internal_mutable_device() {
  
  return _impl_.device_.Mutable(GetArenaForAllocation());
}
inline std::string* AutotuneResults_Entry::release_device() {
  // @@protoc_insertion_point(field_release:xla.AutotuneResults.Entry.device)
  return _impl_.device_.Release();
}
inline void AutotuneResults_Entry::set_allocated_device(std::string* device) {
  if (device != nullptr) {
    
  } else {
    
  }
  _impl_.device_.SetAllocated(device, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.device_.IsDefault()) {
    _impl_.device_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:xla.AutotuneResults.Entry.device)
}

// string hlo = 2;
inline void AutotuneResults_Entry::clear_hlo() {
  _impl_.hlo_.ClearToEmpty();
}
inline const std::string& AutotuneResults_Entry::hlo() const {
  // @@protoc_insertion_point(field_get:xla.AutotuneResults.Entry.hlo)
  return _internal_hlo();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void AutotuneResults_Entry::set_hlo(ArgT0&& arg0, ArgT... args) {
 
 _impl_.hlo_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:xla.AutotuneResults.Entry.hlo)
}
inline std::string* AutotuneResults_Entry::mutable_hlo() {
  std::string* _s = _internal_mutable_hlo();
  // @@protoc_insertion_point(field_mutable:xla.AutotuneResults.Entry.hlo)
  return _s;
}
inline const std::string& AutotuneResults_Entry::_internal_hlo() const {
  return _impl_.hlo_.Get();
}
inline void AutotuneResults_Entry::_internal_set_hlo(const std::string& value) {
  
  _impl_.hlo_.Set(value, GetArenaForAllocation());
}
inline std::string* AutotuneResults_Entry::_internal_mutable_hlo() {
  
  return _impl_.hlo_.Mutable(GetArenaForAllocation());
}
inline std::string* AutotuneResults_Entry::release_hlo() {
  // @@protoc_insertion_point(field_release:xla.AutotuneResults.Entry.hlo)
  return _impl_.hlo_.Release();
}
inline void AutotuneResults_Entry::set_allocated_hlo(std::string* hlo) {
  if (hlo != nullptr) {
    
  } else {
    
  }
  _impl_.hlo_.SetAllocated(hlo, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.hlo_.IsDefault()) {
    _impl_.hlo_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:xla.AutotuneResults.Entry.hlo)
}

// .tensorflow.AutotuneResult result = 3;
inline bool AutotuneResults_Entry::_internal_has_result() const {
  return this != internal_default_instance() && _impl_.result_ != nullptr;
}
inline bool AutotuneResults_Entry::has_result() const {
  return _internal_has_result();
}
inline const ::tensorflow::AutotuneResult& AutotuneResults_Entry::_internal_result() const {
  const ::tensorflow::AutotuneResult* p = _impl_.result_;
  return p != nullptr ? *p : reinterpret_cast<const ::tensorflow::AutotuneResult&>(
      ::tensorflow::_AutotuneResult_default_instance_);
}
inline const ::tensorflow::AutotuneResult& AutotuneResults_Entry::result() const {
  // @@protoc_insertion_point(field_get:xla.AutotuneResults.Entry.result)
  return _internal_result();
}
inline void AutotuneResults_Entry::unsafe_arena_set_allocated_result(
    ::tensorflow::AutotuneResult* result) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.result_);
  }
  _impl_.result_ = result;
  if (result) {
    
  } else {
    
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:xla.AutotuneResults.Entry.result)
}
inline ::tensorflow::AutotuneResult* AutotuneResults_Entry::release_result() {
  
  ::tensorflow::AutotuneResult* temp = _impl_.result_;
  _impl_.result_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::tensorflow::AutotuneResult* AutotuneResults_Entry::unsafe_arena_release_result() {
  // @@protoc_insertion_point(field_release:xla.AutotuneResults.Entry.result)
  
  ::tensorflow::AutotuneResult* temp = _impl_.result_;
  _impl_.result_ = nullptr;
  return temp;
}
inline ::tensorflow::AutotuneResult* AutotuneResults_Entry::_internal_mutable_result() {
  
  if (_impl_.result_ == nullptr) {
    auto* p = CreateMaybeMessage<::tensorflow::AutotuneResult>(GetArenaForAllocation());
    _impl_.result_ = p;
  }
  return _impl_.result_;
}
inline ::tensorflow::AutotuneResult* AutotuneResults_Entry::mutable_result() {
  ::tensorflow::AutotuneResult* _msg = _internal_mutable_result();
  // @@protoc_insertion_point(field_mutable:xla.AutotuneResults.Entry.result)
  return _msg;
}
inline void AutotuneResults_Entry::set_allocated_result(::tensorflow::AutotuneResult* result) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.result_);
  }
  if (result) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(result));
    if (message_arena != submessage_arena) {
      result = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, result, submessage_arena);
    }
    
  } else {
    
  }
  _impl_.result_ = result;
  // @@protoc_insertion_point(field_set_allocated:xla.AutotuneResults.Entry.result)
}

// -------------------------------------------------------------------

// AutotuneResults

// int32 version = 1;
inline void AutotuneResults::clear_version() {
  _impl_.version_ = 0;
}
inline int32_t AutotuneResults::_internal_version() const {
  return _impl_.version_;
}
inline int32_t AutotuneResults::version() const {
  // @@protoc_insertion_point(field_get:xla.AutotuneResults.version)
  return _internal_version();
}
inline void AutotuneResults::_internal_set_version(int32_t value) {
  
  _impl_.version_ = value;
}
inline void AutotuneResults::set_version(int32_t value) {
  _internal_set_version(value);
  // @@protoc_insertion_point(field_set:xla.AutotuneResults.version)
}

// repeated .xla.AutotuneResults.Entry dots = 2;
inline int AutotuneResults::_internal_dots_size() const {
  return _impl_.dots_.size();
}
inline int AutotuneResults::dots_size() const {
  return _internal_dots_size();
}
inline void AutotuneResults::clear_dots() {
  _impl_.dots_.Clear();
}
inline ::xla::AutotuneResults_Entry* AutotuneResults::mutable_dots(int index) {
  // @@protoc_insertion_point(field_mutable:xla.AutotuneResults.dots)
  return _impl_.dots_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::AutotuneResults_Entry >*
AutotuneResults::mutable_dots() {
  // @@protoc_insertion_point(field_mutable_list:xla.AutotuneResults.dots)
  return &_impl_.dots_;
}
inline const ::xla::AutotuneResults_Entry& AutotuneResults::_internal_dots(int index) const {
  return _impl_.dots_.Get(index);
}
inline const ::xla::AutotuneResults_Entry& AutotuneResults::dots(int index) const {
  // @@protoc_insertion_point(field_get:xla.AutotuneResults.dots)
  return _internal_dots(index);
}
inline ::xla::AutotuneResults_Entry* AutotuneResults::_internal_add_dots() {
  return _impl_.dots_.Add();
}
inline ::xla::AutotuneResults_Entry* AutotuneResults::add_dots() {
  ::xla::AutotuneResults_Entry* _add = _internal_add_dots();
  // @@protoc_insertion_point(field_add:xla.AutotuneResults.dots)
  return _add;
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::AutotuneResults_Entry >&
AutotuneResults::dots() const {
  // @@protoc_insertion_point(field_list:xla.AutotuneResults.dots)
  return _impl_.dots_;
}

// repeated .xla.AutotuneResults.Entry convs = 3;
inline int AutotuneResults::_internal_convs_size() const {
  return _impl_.convs_.size();
}
inline int AutotuneResults::convs_size() const {
  return _internal_convs_size();
}
inline void AutotuneResults::clear_convs() {
  _impl_.convs_.Clear();
}
inline ::xla::AutotuneResults_Entry* AutotuneResults::mutable_convs(int index) {
  // @@protoc_insertion_point(field_mutable:xla.AutotuneResults.convs)
  return _impl_.convs_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::AutotuneResults_Entry >*
AutotuneResults::mutable_convs() {
  // @@protoc_insertion_point(field_mutable_list:xla.AutotuneResults.convs)
  return &_impl_.convs_;
}
inline const ::xla::AutotuneResults_Entry& AutotuneResults::_internal_convs(int index) const {
  return _impl_.convs_.Get(index);
}
inline const ::xla::AutotuneResults_Entry& AutotuneResults::convs(int index) const {
  // @@protoc_insertion_point(field_get:xla.AutotuneResults.convs)
  return _internal_convs(index);
}
inline ::xla::AutotuneResults_Entry* AutotuneResults::_internal_add_convs() {
  return _impl_.convs_.Add();
}
inline ::xla::AutotuneResults_Entry* AutotuneResults::add_convs() {
  ::xla::AutotuneResults_Entry* _add = _internal_add_convs();
  // @@protoc_insertion_point(field_add:xla.AutotuneResults.convs)
  return _add;
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::xla::AutotuneResults_Entry >&
AutotuneResults::convs() const {
  // @@protoc_insertion_point(field_list:xla.AutotuneResults.convs)
  return _impl_.convs_;
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace xla

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tensorflow_2fcompiler_2fxla_2fautotune_5fresults_2eproto
